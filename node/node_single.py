from fastapi import FastAPI, Response, status
from pydantic import BaseModel

import storage

app = FastAPI()


class Item(BaseModel):
    key: str
    value: str


@app.post("/", status_code=201)
async def set_kv(item: Item, response: Response):
    if storage.get(item.key) is not None:
        response.status_code = status.HTTP_200_OK
    storage.set(item.key, item.value)
    return item.dict()


@app.get("/", status_code=200)
async def get_kv(key: str, response: Response):
    value = storage.get(key)
    if value is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return value
    return value


@app.delete("/", status_code=200)
async def del_kv(key: str, response: Response):
    deleted: bool = storage.delete(key)
    if not deleted:
        response.status_code = status.HTTP_404_NOT_FOUND
    return '{}'