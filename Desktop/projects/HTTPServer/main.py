from socket import  *
import sys
import os
import threading


#CONSTANTS
server = '127.0.0.1'
PORT = 8000
FORMAT = "utf-8"


class TCPServer():

    def __init__(self,host='127.0.0.1',port=8000):
        self.host = host
        self.port = port

    def startServer(self):

        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serverSocket.bind((self.host,self.port))
        serverSocket.listen()
        print('Listening on port %s ...' % PORT)

        while True:
            print("Server started!!")
            print("\n+++++++ Waiting for new connection ++++++++\n\n");
            try:
                connectionSocket, addr = serverSocket.accept()
                request = connectionSocket.recv(1024).decode(FORMAT)
                print("This is the message by cient: "+request)

                # Parse HTTP headers
                headers = request.split('\n')
                filename = headers[0].split()[1]

                # Get the content of the file
                if filename == '/':
                    filename = '/index.html'

                try:
                    fin = open('htdocs' + filename)
                    content = fin.read()
                    fin.close()

                    response = self.hanle_request(content)
                except FileNotFoundError:
                    response = 'HTTP/1.0 404 NOT FOUND\n\n<h1>File Not Found</h1>'
                finally:

                    # Send HTTP response
                    connectionSocket.sendall(response.encode())
                    connectionSocket.close()

            except:
                print("Server Closed")
                break

    def hanle_request(self,data):
            return data


class HTTPServer(TCPServer):

    def hanle_request(self,data):
        response_line = "HTTP/1.1 200 OK\r\n"

        blank_line = "\r\n"

        response_body = data

        return response_line+blank_line+response_body


if __name__ =='__main__':
    server = HTTPServer()
    server.startServer()
