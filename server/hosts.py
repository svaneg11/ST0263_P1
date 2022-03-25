import os
import pickle
import platform
import sys
from pathlib import Path
from .hashing import assign_hash_ranges


PARTITIONS = 16384

hosts = []

OS = platform.system()
conf_path: Path
if OS == 'Windows':
    conf_path = Path.home() / 'AppData' / 'Local' / 'p1'
elif OS == 'Linux':
    conf_path = '/etc' / 'p1'


def set_remote_nodes(nodes):
    ip = []
    ports = []
    for h in nodes:
        ip.append(h[0])
        ports.append(h[1])
    print(ip, ports)
    global hosts
    hosts = assign_hash_ranges(ip, ports)
    create_server_dir()
    save_hosts()


def create_server_dir():
    os.makedirs(conf_path, exist_ok='True')
    server_path = conf_path / f'server'
    if not server_path.is_dir():  # Check if folder exists
        os.mkdir(server_path)


def save_hosts():
    global conf_path
    hosts_file = open(conf_path / 'server' / 'hosts', 'wb')
    pickle.dump(hosts, hosts_file)
    hosts_file.close()


def load_hosts():
    global hosts, conf_path
    try:
        hosts_file = open(conf_path / 'server' / 'hosts', 'rb')
        hosts = pickle.load(hosts_file)
        hosts_file.close()
    except FileNotFoundError:
        print('You have to set the hosts before starting the proxy server!')
        sys.exit(1)
    return hosts

#hosts = [{'host': '127.0.0.2', 'port': '2000', 'partition': 0, 'hash_range': (1, 5461)}, ...]