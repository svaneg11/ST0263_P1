from typing import List, Dict
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

import node.storage as storage

app = FastAPI()


class Item(BaseModel):
    hash: str
    key: str
    value: str


class MultipleItems(BaseModel):
    items: List[Item]


class HashKey(BaseModel):
    hash: str
    key: str

class HKList(BaseModel):
    items: List[HashKey]

@app.post("/", status_code=201)
async def set_kv(item: Item, response: Response):
    if storage.get(item.hash, item.key) is not None:
        response.status_code = status.HTTP_200_OK
    storage.set(item.hash, item.key, item.value)
    return item.dict()


@app.get("/", status_code=200)
async def get_kv(hash: str, key: str, response: Response):
    value = storage.get(hash, key)
    if value is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return value
    return value


@app.delete("/", status_code=200)
async def del_kv(hash: str, key: str, response: Response):
    deleted: bool = storage.delete(hash, key)
    if not deleted:
        response.status_code = status.HTTP_404_NOT_FOUND
    return deleted


# Multi operations.
@app.post("/m", status_code=200)
async def mset_kv(items: MultipleItems):
    storage.multiple_set(items.items)
    return [item.dict() for item in items.items]


@app.get("/m", status_code=200)
async def mget_kv(items: HKList):
    all_success, response_items, not_found = storage.multiple_get(items.items)
    res = {'all_success': all_success, 'response_items': response_items, 'not_found': not_found}
    return res


@app.delete("/m", status_code=200)
async def mdel_kv(items: HKList):
    all_deleted, response_items, not_found = storage.multiple_del(items.items)
    res = {'all_deleted': all_deleted, 'deleted_items': response_items, 'not_found': not_found}
    return res


# @app.get("/m", status_code=200)
# async def get_kv(hash: str, key: str, response: Response):
#     value = storage.get(hash, key)
#     if value is None:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return value
#     return value
#
#
# @app.delete("/m", status_code=200)
# async def del_kv(hash: str, key: str, response: Response):
#     deleted: bool = storage.delete(hash, key)
#     if not deleted:
#         response.status_code = status.HTTP_404_NOT_FOUND
#     return deleted
#
