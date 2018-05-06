import json


class Configuration(object):
    def __init__(self):
        self.nodes = {}

    def load(self):
        with open('cluster.json') as f:
            self.nodes = json.load(f)
