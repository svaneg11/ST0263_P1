from setup_node import setup
import sys

def main(argv):
    if len(argv) > 1:
        if argv[1] == "-p":
            setup(int(argv[2]))
        elif argv[1] == "-help":
            print("Use -p ## -> with ## being a port number to setup a server in the localhost and \n\t     the port mentioned.")
    else: 
        print("Use -help to get information about the accepted comands.")

if __name__ == "__main__":
    main(sys.argv)