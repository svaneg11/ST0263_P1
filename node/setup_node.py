import config
import storage
import uvicorn
from node_server import app


def setup(port):
    config.set_port(port)
    config.create_conf_dir()
    storage.load()
    uvicorn.run(app=app, host="127.0.0.1", port=port, log_level="info")