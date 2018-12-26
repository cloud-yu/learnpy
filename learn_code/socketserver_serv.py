from socketserver import (TCPServer as TCP, StreamRequestHandler as SRH)
from time import ctime
import os

HOST = ''
PORT = 21567
ADDR = (HOST, PORT)


class MyRequestHandler(SRH):

    def handle(self):
        print('...connected from:', self.client_address)
        # self.wfile.write(bytes('[%s] %s ' % (ctime(), self.rfile.readline().decode('utf-8')), encoding='utf-8'))
        self.data = self.rfile.readline().strip()
        print('Recv: %s' % self.data)
        if str(self.data, 'utf-8') == 'date':
            self.wfile.write(bytes(ctime(), 'utf-8'))
        if str(self.data, 'utf-8') == 'os':
            self.wfile.write(bytes(os.name, 'utf-8'))
        if str(self.data, 'utf-8') == 'ls':
            self.wfile.write(bytes('\n'.join(os.listdir()), 'utf-8'))


tcpServ = TCP(ADDR, MyRequestHandler)
print('waiting for connection...')
tcpServ.serve_forever()