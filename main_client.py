from requests import get, post, delete
import sys
from colorama import Style, Fore
from json import dumps

class Client:
    def __init__(self, host, port):
        self.host = "http://" +  str(host) + ":" + str(port)
        self.connect()

    def connect(self):
        response = get(self.host+"/?key=XX")
        if (str(response)[11:-2] == "404" or str(response)[11:-2] == "200"):
            
            mns = self.host[7:len(self.host)] + " -> "

            while True:
                peticion = input(Fore.GREEN + mns + Style.RESET_ALL)

                lista_peticion = peticion.split(" ")
                lista_peticion[0].lower()

                if (lista_peticion[0] == "out"):
                    break
                elif (lista_peticion[0] == "get"):
                    print(self.get(lista_peticion[1]))
                elif (lista_peticion[0] == "set"):
                    print(self.set(lista_peticion[1], " ".join(lista_peticion[2:len(lista_peticion)])))
                elif (lista_peticion[0] == "delete"):
                    print (self.eliminar(lista_peticion[1]))
                else:
                    print("Please enter a valid command")

        else:
            print ("Couldn't connect to the server")

    def get(self, key):
        string = self.host + "/?key=" + key
        response = get(string)
        return response.text

    def set(self, key, valor):
        dato = {"key": str(key), "value": str(valor)}
        response = post(self.host+"/", data=dumps(dato))
        return response.text
    
    def eliminar(self, key):
        string = self.host + "/?key=" + key
        response = delete(string)
        return response.text

# ------------------------------------------------------------------------------------------------------------

def main(argv):
    if ("-p" in argv):
        port = argv[argv.index("-p")+1]
        if ("-h" in argv):
            host = argv[argv.index("-h")+1]
        else:
            host = "localhost"
        print("PORT: ",port)
        print("HOST: ",host)

        c = Client(host, port)
    else:
        print("Please indicate the desire port with -p #")

if __name__ == "__main__":
    main(sys.argv)