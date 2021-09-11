import sys
import struct
import socket

server = '8.8.8.8'
serverPort = 53
no_args = len(sys.argv)
if no_args < 2:
    print("The format is 'python3 mywget.py hostname1 '")

hostnames = sys.argv[1:]

def recvall(sock):
    BUFF_SIZE = 4096
    data = bytearray()
    while True:
        packet = sock.recv(BUFF_SIZE)
        if not packet:
            break
        data.extend(packet)
    return data

for hostname in hostnames:

    query = bytes("\x12\x12" +
                  "\x00\x00" +
                  "\x00\x01" +
                  "\x00\x00" +
                  "\x00\x00" +
                  "\x00\x00", 'utf-8')

    d = bytes("", 'utf-8')

    for a in hostname.split('.'):
        d += struct.pack("!b" + str(len(a)) + "s", len(a), bytes(a, "utf-8"))

    query = query + d + bytes("\x00", 'utf-8')  # terminate domain with zero len

    query = query + bytes("\x00\x01" + "\x00\x01", 'utf-8')  # type A, class IN

    while (1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(query, (server, serverPort))
        reply, addr = sock.recvfrom(2048)

        x = ""
        y = len(reply)
        for i in range(y-4, len(reply)):
            x += str(reply[i])
            x += "."
        x = x[:len(x) - 1]

        if(len(reply) > len(query)):
            break

    """---------------HTTPCLIENT------------"""

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((x, 80))

    message = "GET / HTTP/1.1\r\n"
    message += "HOST:"+ hostname +"\r\n"
    message += "User-Agent: Firefox/86\r\n"
    message += "\r\n"
    x = s.send(message.encode())

    data = recvall(s).decode()

    i = 0
    s = ""
    code = "HTTP/1.1 302"
    while(data[i] != "<"):
        s += data[i]
        i +=1
    if s.find(code) != -1:
         print(s)
    else:
        data = data.replace(s,"")
        with open("index"+"."+hostname+".html", "w") as f:
            f.write(data)
