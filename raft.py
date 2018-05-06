import threading


class Raft(object):

    def __init__(self, configuration, state):
        self.configuration = configuration
        self.state = state
        self.election_timer = None

    def parse_json_request(self, json_message):
        print('received message:', json_message)

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
        self.election_timer = threading.Timer(1, self.handle_election_timeout)
        self.election_timer.start()

    def handle_election_timeout(self):
        print('election timeout!')
