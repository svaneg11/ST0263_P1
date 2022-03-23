from urllib import request
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

import storage
import cluster_storage

from requests import get, post, delete
from json import dumps

app = FastAPI()

class Item(BaseModel):
    key: str
    value: str


@app.post("/", status_code=201)
async def set_kv(item: Item, response: Response):
    i = cluster_storage.redirect(item.key)
    string = "http://localhost:" + i
    request = string+ "/?key=" + item.key
    response = get(request.replace(" ",""))
    if response.text is not None:
        response.status_code = status.HTTP_200_OK

    dato = {"key": str(item.key), "value": str(item.value)}
    request2 = string+"/"
    response2 = post(request2.replace(" ",""), data=dumps(dato))
    return response2.text


@app.get("/", status_code=200)
async def get_kv(key: str, response: Response):
    i = cluster_storage.redirect(key)
    string = "http://localhost:" + i
    request = string + "/?key=" + key
    response = get(request.replace(" ",""))
    if str(response)[11:-2] == "404":
        response.status_code = status.HTTP_404_NOT_FOUND
        return response.text
    return response.text


@app.delete("/", status_code=200)
async def del_kv(key: str, response: Response):
    i = cluster_storage.redirect(key)
    string = "http://localhost:" + i
    request = string+ "/?key=" + key
    response = delete(request.replace(" ",""))
    if str(response)[11:-2] == "404":
        response.status_code = status.HTTP_404_NOT_FOUND
    return '{}'