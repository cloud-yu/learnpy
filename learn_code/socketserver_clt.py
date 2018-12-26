import socket

HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

while True:
    tcpClisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpClisock.connect(ADDR)
    data = input('>')
    if not data:
        break

    tcpClisock.send(bytes('%s\r\n' % data, encoding='utf-8'))
    data = tcpClisock.recv(BUFSIZ)
    if not data:
        break
    print(data.decode('utf-8'))
    tcpClisock.close()