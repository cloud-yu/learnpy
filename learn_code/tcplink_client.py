import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 9999))
time.sleep(3)
print(s.recv(1024).decode('utf-8'))

for data in [b'Michael', b'Tracy', b'Sarah']:
    s.send(data)
    time.sleep(3)
    print(s.recv(1024).decode('utf-8'))

s.send(b'exit')
s.close()
