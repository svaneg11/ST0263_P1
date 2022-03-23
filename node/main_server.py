import sys
import config
import storage
import uvicorn
import cluster_storage

from node_single import app
from node_server import app as appS

def main(argv):
    if len(argv) > 1:
        if argv[1] == "-p":
            config.set_port(int(argv[2]))
            config.create_conf_dir()
            storage.load()
            uvicorn.run(app=app, host="127.0.0.1", port=int(argv[2]), log_level="info")
        elif argv[1] == "-help":
            print("Use -p ## -> with ## being a port number to setup a server in the localhost and \n\t     the port mentioned.")
        elif argv[1] == "-c":
            config.set_port(int(argv[2]))
            config.create_conf_dir()
            config.create_clust_dir(str(argv[3]))
            i = cluster_storage.load(str(argv[3]))
            if (i):
                node = input("Enter a port to add to the cluster: ")
                while (node != "stop"):
                    cluster_storage.add(node)
                    node = input("Enter a port to add to the cluster: ")

            cluster_storage.define_ranges()
            middle.Middle()
            uvicorn.run(app=appS, host="127.0.0.1", port=int(argv[2]), log_level="info")
    else: 
        print("Use -help to get information about the accepted comands.")

if __name__ == "__main__":
    main(sys.argv)