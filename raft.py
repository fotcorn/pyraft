import math
import random
import aiohttp
import asyncio
from messages import AppendEntryRequest, AppendEntryResponse, RequestVoteRequest, RequestVoteResponse
from timer import Timer


class Raft(object):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3

    def __init__(self, node_name, configuration, state):
        self.node_name = node_name
        self.configuration = configuration
        self.type = Raft.FOLLOWER
        self.state = state
        self.election_timer = None
        self.election_timeout = 2 + random.randint(0, 3)
        self.leader_timer = None
        self.leader_timeout = 0.25
        self.vote_set = set()

    def log(self, message, *args):
        if self.type == Raft.FOLLOWER:
            t = 'follower'
        elif self.type == Raft.CANDIDATE:
            t = 'candidate'
        else:
            t = 'leader'
        print('{} ({}):'.format(self.node_name, t), message.format(*args))

    def parse_json_request(self, json_message):
        if json_message['type'] == RequestVoteRequest.MESSAGE_TYPE:
            message = RequestVoteRequest(**json_message['data'])
            return self.serialize_message(self.handle_vote_request(message))
        elif json_message['type'] == AppendEntryRequest.MESSAGE_TYPE:
            message = AppendEntryRequest(**json_message['data'])
            return self.serialize_message(self.handle_append_entry_request(message))

    def parse_json_response(self, request, json_message, node_name):
        if json_message['type'] == RequestVoteResponse.MESSAGE_TYPE:
            message = RequestVoteResponse(**json_message['data'])
            self.handle_vote_response(message, node_name)
        elif json_message['type'] == AppendEntryResponse.MESSAGE_TYPE:
            message = AppendEntryResponse(**json_message['data'])
            self.handle_append_entry_response(request, message, node_name)

    def serialize_message(self, message):
        data = {}
        data['data'] = message.__dict__.copy()
        data['type'] = message.MESSAGE_TYPE
        return data

    def send_message(self, node_name, message):
        node = self.configuration.nodes[node_name]
        url = 'http://{}:{}'.format(node['host'], node['port'])
        asyncio.ensure_future(self._send(url, node_name, message))

    async def _send(self, url, node_name, message):
        data = self.serialize_message(message)
        async with aiohttp.request('POST', url, json=data) as resp:
            response = await resp.json()
            self.parse_json_response(message, response, node_name)

    def handle_vote_request(self, message: RequestVoteRequest):
        self.log('received vote request from {}', message.candidate)
        if message.term > self.state.current_term:
            self.state.current_term = message.term
            self.state.voted_for = None
        if message.term < self.state.current_term or self.state.voted_for is not None:
            return RequestVoteResponse(self.state.current_term, False)
        # TODO: check message.last_log_index, message.last_log_term
        self.state.voted_for = message.candidate
        return RequestVoteResponse(self.state.current_term, True)

    def handle_vote_response(self, response, node_name):
        self.log('received vote response from {}, vote_granted: {}', node_name, response.vote_granted)
        if response.term > self.state.current_term:
            self.step_down()
            self.state.current_term = response.term
            self.state.voted_for = None
            return

        if not self.type == Raft.LEADER and response.vote_granted:
            self.vote_set.add(node_name)
            if len(self.vote_set) >= math.ceil(len(self.configuration.nodes) / 2):
                self.type = Raft.LEADER
                self.log('We have been elected leader')
                self.election_timer.cancel()
                self.handle_leader_timeout()

    def handle_append_entry_request(self, message):
        self.log('received append entry request')
        self.reset_election_timer()
        self.type = Raft.FOLLOWER
        if self.leader_timer:
            self.leader_timer.cancel()
            self.leader_timer = None
        # TODO: append data
        # TODO check term
        return AppendEntryResponse(self.state.current_term, True)

    def handle_append_entry_response(self, request, response, node_name):
        self.log('received append entry response from {}', node_name)
        # TODO: update next_index, match_index

    def step_down(self):
        self.log('Stepping down...')
        self.type = Raft.FOLLOWER
        if self.leader_timer:
            self.leader_timer.cancel()
            self.leader_timer = None

    def reset_election_timer(self):
        if self.election_timer:
            self.election_timer.cancel()
        self.election_timer = Timer(self.election_timeout, self.handle_election_timeout)

    def handle_election_timeout(self):
        self.log('Election timeout, switching to candidate state')
        self.type = Raft.CANDIDATE
        self.state.current_term += 1
        self.state.voted_for = self.node_name
        self.vote_set = {self.node_name}

        message = RequestVoteRequest(self.state.current_term, self.node_name, 0, 0)
        for node_name in self.configuration.nodes.keys():
            if node_name == self.node_name:
                continue
            self.send_message(node_name, message)
        self.reset_election_timer()

    def handle_leader_timeout(self):
        self.log('Leader timeout, sending heartbeat message')
        message = AppendEntryRequest(self.state.current_term, self.node_name, 0, 0, None, None, self.state.commit_index)
        for node_name in self.configuration.nodes.keys():
            if node_name == self.node_name:
                continue
            self.send_message(node_name, message)

        self.leader_timer = Timer(self.leader_timeout, self.handle_leader_timeout)
