import os
import platform
from pathlib import Path
from sys import exit

port = None
OS = platform.system()
if OS == 'Windows':
    conf_path = Path.home() / 'AppData' / 'Local' / 'p1'
elif OS == 'Linux':
    conf_path = '/etc' / 'p1'


def set_port(num):
    global port
    try:
        int(num)
    except Exception:
        print("Port number can't have letters/symbols")
        exit(0)
    port = str(num)


def create_conf_dir():
    os.makedirs(conf_path, exist_ok='True')
    node_path = conf_path / f'node-{port}'
    if not node_path.is_dir():     # Check if folder exists
        os.mkdir(node_path)

def create_clust_dir(name):
    os.makedirs(conf_path, exist_ok='True')
    clust_path = conf_path / f'node-{port}' / f'cluster-{name}'
    if not clust_path.is_dir():     # Check if folder exists
        os.mkdir(clust_path)

def get_data_path():
    data_path = conf_path / f'node-{port}' / 'dbfile'
    return data_path

def get_cluster_path(name):
    data_path = conf_path / f'node-{port}' / f'cluster-{name}' / 'dbfile'
    return data_path