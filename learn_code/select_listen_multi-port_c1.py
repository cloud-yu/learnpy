import socket
from multiprocessing import Pool


def connect(port):
    obj = socket.socket()
    obj.connect(('127.0.0.1', port))

    content = str(obj.recv(1024), encoding='utf-8')
    print(content)

    obj.close()


if __name__ == '__main__':
    p = Pool(2)
    portlist = [8001, 8002, 8003]
    for port in portlist:
        p.apply_async(connect, args=(port, ))
    p.close()
    p.join()
    print('ALL Done')