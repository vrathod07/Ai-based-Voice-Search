import socket
import sys
from socket import  *
from threading import *

#consatnts
server = "localhost"
PORT = 5005
FORMAT = "utf-8"
mess = "Hello Server how are you!"


def serve():

    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((server, PORT))
        clientSocket.send(mess.encode(FORMAT))

    except:
        print("disconnected")
        clientSocket.close()
        sys.exit(0)

serve()