import sys
import argparse

from node.setup_node import setup
from server.hosts import set_remote_nodes, load_hosts
from server.proxy_server import run


parser = argparse.ArgumentParser()

# setup
parser.add_argument('type', choices=['node', 'server'],
                    help='Setup a node server or a proxy server', metavar='type', type=str)

parser.add_argument('port',
                    help='Specify the port where the server will listen.', metavar='port', type=int)

parser.add_argument('-n', action='append', nargs=2, dest='nodes',
                    help='The proxy server uses this IP and port to connect with the db node',
                    metavar=('host', 'port'))

parser.add_argument('--start', action='store_true',
                    help='Used with server to start it loading the server config, if present',
                    required=False)


args = parser.parse_args()


if args.type == 'node':
    setup(args.port)
elif args.type == 'server':
    if args.start:
        run(args.port)
    elif len(args.nodes) >= 2:
        set_remote_nodes(args.nodes)
    else:
        print('Remote nodes information required.')
        sys.exit(1)
