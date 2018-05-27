import sys

from configuration import Configuration
from http_server import HttpServer
from state import State
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
    server = HttpServer(raft.parse_json_request)
    server.run(configuration.nodes[node_name]['port'])


if __name__ == '__main__':
    main()
