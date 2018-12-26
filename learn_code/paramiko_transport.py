import paramiko
import sys
import select
import socket
import threading

# 建立一个socket
trans = paramiko.Transport(('127.0.0.1', 33322))
# trans = paramiko.Transport(('10.190.24.213', 22))
# 启动一个客户端
trans.start_client()

# 如果使用rsa密钥登录的话
# '''
# default_key_file = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
# prikey = paramiko.RSAKey.from_private_key_file(default_key_file)
# trans.auth_publickey(username='super', key=prikey)
# '''
# 如果使用用户名和密码登录
# trans.auth_password(username='dev650', password='1234qwer')
trans.auth_password(username='archie', password='archie')
# 打开一个通道
channel = trans.open_session()
# 获取终端
channel.get_pty(term='xterm')
# 激活终端，这样就可以登录到终端了，就和我们用类似于xshell登录系统一样
channel.invoke_shell()
# 下面就可以执行你所有的操作，用select实现
# 对输入终端sys.stdin和 通道进行监控,
# 当用户在终端输入命令后，将命令交给channel通道，这个时候sys.stdin就发生变化，select就可以感知
# channel的发送命令、获取结果过程其实就是一个socket的发送和接受信息的过程

# windows下select只能接受socket作为输入监听，sys.stdin不能直接作为输入，需要建立一个socket监听sys.stdin
sk1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sk1.bind(('127.0.0.1', 9900))

sk2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_msg(sk2):
    while True:
        data = sys.stdin.read(1)

        sk2.sendall(data)


# def recv_msg(sk1):
#     while True:
#         data, addr = sk1.recvfrom(1)
#         channel.sendall(data)

threading.Thread(target=send_msg, args=(channel, )).start()
# threading.Thread(target=recv_msg, args=(sk1, )).start()

while True:
    readlist, writelist, errlist = select.select([
        channel,
    ], [], [])
    # 如果是用户输入命令了,sys.stdin发生变化
    # if sk1 in readlist:
    #     # 获取输入的内容
    #     input_cmd = sys.stdin.read(1)
    #     # 将命令发送给服务器
    #     channel.sendall(input_cmd)

    # 服务器返回了结果,channel通道接受到结果,发生变化 select感知到
    if channel in readlist:
        # 获取结果
        result = channel.recv(1024)
        # 断开连接后退出
        if len(result) == 0:
            print("\r\n**** EOF **** \r\n")
            break

        # 输出到屏幕
        sys.stdout.write(result.decode('utf-8'))
        sys.stdout.flush()

    # 关闭通道
channel.close()
# 关闭链接
trans.close()