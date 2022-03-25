import requests
import uvicorn

from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from .hosts import load_hosts
from .hashing import crc16_hash

hosts = []
num_hosts = len(hosts)
print(hosts, num_hosts)
app = FastAPI()


class Item(BaseModel):
    key: str
    value: str


def select_node(key):
    partition, hash_slot = crc16_hash(key, num_hosts)
    node = hosts[partition]
    url = f"http://{node['host']}:{node['port']}/"
    return url, str(hash_slot), f"{node['host']}:{node['port']}"


@app.post("/", status_code=201)
async def set_kv(item: Item, response: Response):
    url, hash_slot, node = select_node(item.key)
    obj = {'hash': hash_slot}
    obj.update(item.dict())
    r = requests.post(url, json=obj)
    response.status_code = r.status_code
    res = r.json()
    res.update({"db_node": node})
    return res


@app.get("/", status_code=200)
async def get_kv(key: str, response: Response):
    url, hash_slot, node = select_node(key)
    obj = {'hash': hash_slot}
    obj.update({'key': key})
    r = requests.get(url, params=obj)
    response.status_code = r.status_code
    res = r.json()
    res = {'value': res}
    if res is not None:
        res.update({"hash": hash_slot, "db_node": node})
    return res


@app.delete("/", status_code=200)
async def del_kv(key: str, response: Response):
    url, hash_slot, node = select_node(key)
    obj = {'hash': hash_slot}
    obj.update({'key': key})
    r = requests.delete(url, params=obj)
    response.status_code = r.status_code
    return {"deleted": r.text, "db_node": node}


def run(port):
    global hosts, num_hosts
    hosts = load_hosts()
    num_hosts = len(hosts)
    uvicorn.run(app=app, host="127.0.0.1", port=port, log_level="info")