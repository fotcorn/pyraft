import json


class State(object):
    def __init__(self):
        self.current_term = None
        self.voted_for = None
        self.log = []
        self.last_applied = 0
        self.commit_index = 0
        self.next_index = {}
        self.match_index = {}

    def load(self, node_name):
        with open('{}.json'.format(node_name)) as f:
            config = json.load(f)
        self.current_term = config['current_term']
        self.voted_for = config['voted_for']
        self.log = config['log']
        self.last_applied = len(self.log)
        self.commit_index = 0

    def reset_leader_data(self):
        self.next_index = {}
        self.match_index = {}
