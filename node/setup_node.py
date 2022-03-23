import socket
import node.config as config
import uvicorn
from node.node_server import app


def setup(port):
        config.set_port(port)
        config.create_conf_dir()
        uvicorn.run(app=app, host="127.0.0.1", port=port, log_level="info")


