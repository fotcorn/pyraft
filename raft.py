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
        self.election_timeout = 0.5 + random.randint(0, 1000) / 1000.0
        self.leader_timer = None
        self.leader_timeout = 0.25

    def log(self, message, *args):
        print('{}:'.format(self.node_name), message.format(args))

    def parse_json_request(self, json_message):
        self.log('received message: {}', json_message)

    def send_message(self, node_name, message):
        data = {}
        data['data'] = message.__dict__.copy()
        data['type'] = message.MESSAGE_TYPE
        node = self.configuration.nodes[node_name]
        url = 'http://{}:{}'.format(node['host'], node['port'])
        asyncio.ensure_future(self._send(url, data))

    async def _send(self, url, data):
        async with aiohttp.request('POST', url, json=data) as resp:
            await resp.json()

    def handle_vote_request(self, message):
        pass

    def handle_vote_response(self, message):
        pass

    def handle_append_entry_request(self, message):
        self.reset_election_timer()
        self.type = Raft.FOLLOWER
        if self.leader_timer:
            self.leader_timer.cancel()
            self.leader_timer = None
        # TODO: append data

    def handle_append_entry_response(self, message):
        pass

    def reset_election_timer(self):
        if self.election_timer:
            self.election_timer.cancel()
        self.election_timer = Timer(self.election_timeout, self.handle_election_timeout)

    def handle_election_timeout(self):
        self.log('Election timeout, switching to candidate state')
        self.type = Raft.CANDIDATE
        self.state.current_term += 1
        self.state.voted_for = self.node_name
        message = RequestVoteRequest(self.state.current_term, self.node_name, 0, 0)
        for node_name in self.configuration.nodes.keys():
            if node_name == self.node_name:
                continue
            self.send_message(node_name, message)
