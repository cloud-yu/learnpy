import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 9999))

print('Waiting for connection...')

while True:
    data, addr = s.recvfrom(1024)

    print('Received from %s:%s' % addr)
    print('send %s to %s:%s' % (data, addr[0], addr[1]))
    s.sendto(b'Hello, %s!' % data, addr)
