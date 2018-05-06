import threading
import random
from messages import AppendEntryRequest, AppendEntryResponse, RequestVoteRequest, RequestVoteResponse

class Raft(object):

    def __init__(self, node_name, configuration, state):
        self.node_name = node_name
        self.configuration = configuration
        self.state = state
        self.election_timer = None
        self.election_timeout = 0.5 + random.randint(0, 1000) / 1000.0

    def log(self, message, *args):
        print('{}:'.format(self.node_name), message.format(args))

    def parse_json_request(self, json_message):
        self.log('received message: {}', json_message)

    def send_message(self, message):
        pass

    def handle_vote_request(self, message):
        pass

    def handle_vote_response(self, message):
        pass

    def handle_append_entry_request(self, message):
        pass

    def handle_append_entry_response(self, message):
        pass

    def reset_election_timer(self):
        if self.election_timer:
            self.election_timer.cancel()
        self.election_timer = threading.Timer(self.election_timeout, self.handle_election_timeout)
        self.election_timer.start()

    def handle_election_timeout(self):
        self.log('election timeout')
