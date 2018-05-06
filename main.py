import sys
import os

from configuration import Configuration
from state import State
from http_server import serve_forever
from raft import Raft


def main():
    if len(sys.argv) != 2:
        print('Usage: python main.py <node_name>')
        sys.exit(1)

    node_name = sys.argv[1]

    configuration = Configuration()
    configuration.load()
    if node_name not in configuration.nodes.keys():
        print('Node {} is not in cluster.conf'.format(node_name))
        sys.exit(1)

    state = State()
    state.load(node_name)

    raft = Raft(node_name, configuration, state)

    raft.reset_election_timer()
    serve_forever(raft.parse_json_request)


if __name__ == '__main__':
    main()
