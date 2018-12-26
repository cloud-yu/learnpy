import socket
import select

sk1 = socket.socket()
sk1.bind(('0.0.0.0', 8001))
sk1.listen()

sk2 = socket.socket()
sk2.bind(('0.0.0.0', 8002))
sk2.listen()

sk3 = socket.socket()
sk3.bind(('0.0.0.0', 8003))
sk3.listen()

inputs = [
    sk1,
    sk2,
    sk3,
]

while True:
    r_list, w_list, e_list = select.select(inputs, [], inputs, 1)
    for sk in r_list:
        # conn表示每一个连接对象
        conn, address = sk.accept()
        (lhost, lport) = conn.getsockname()
        (rhost, rport) = conn.getpeername()
        conn.sendall(
            bytes(
                'hello %s:%s, this is %s:%s' % (rhost, rport, lhost, lport),
                encoding='utf-8'))
        conn.close()

    for sk in e_list:
        inputs.remove(sk)