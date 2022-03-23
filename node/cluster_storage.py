from asyncio.windows_events import NULL
from unicodedata import name
import config 
import pickle

cluster = {}

def add(port):
    global cluster
    cluster[port] = 0 
    save()

def define_ranges():
    j = 1
    size = len(cluster)
    for i in cluster:
        cluster[i] = int(2048/(size)) * j 
        j = j + 1
    cluster[i] = 2048
    print(cluster)
    save()

def redirect(key):
    hashed = hash(key)
    if hashed < 0:
        hashed = hashed * -1
    val = int(hashed/2**20)
    for i in cluster:
        if cluster[i] > val:
            break
    print("redirecting to node -> ", i)
    return i

def save():
    cluster_file = open(config.get_cluster_path(nameG), 'wb')
    pickle.dump(cluster, cluster_file)
    cluster_file.close()

def load(name):
    global cluster, cluster_file, nameG
    nameG = name

    try:
        cluster_file = open(config.get_cluster_path(name), 'rb')
        cluster = pickle.load(cluster_file)
        cluster_file.close()
        return False

    except FileNotFoundError:
        cluster = {}
        return True