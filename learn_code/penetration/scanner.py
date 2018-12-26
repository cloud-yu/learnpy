import optparse
import socket
import threading
# 创建进程锁
screenLock = threading.Lock()


def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send(b'ViolentPython\r\n')
        results = connSkt.recv(100)
        # 多线程时防止打印乱序，对打印操作加锁
        screenLock.acquire()
        print('[+] %d tcp open' % tgtPort)
        print('[+] %s' % str(results))
    except:
        # 多线程时防止打印乱序，对打印操作加锁
        screenLock.acquire()
        print('[-] %d tcp closed' % tgtPort)
    finally:
        # 释放线程锁
        screenLock.release()
        connSkt.close()


def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = socket.gethostbyname(tgtHost)
    except:
        print('[-] Cannot resolve "%s" : Unknown host' % tgtHost)
        return
    try:
        tgtName = socket.gethostbyaddr(tgtIP)
        print('[+] Scan Results for : %d' % tgtName[0])
    except:
        print('[+] Scan Results for : %s' % tgtIP)
    socket.setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        # print('Scanning port %s' % tgtPort)
        # connScan(tgtHost, int(tgtPort))
        # ‘’’使用多线程改写
        t = threading.Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()


def main():
    parser = optparse.OptionParser(
        "usage: %prog -H <target host> -p <target port>")
    parser.add_option('-H', dest='tgtHost', type='string',
                      help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string',
                      help='specify target port[s] separated by comma')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(',')
    if (tgtHost is None) | (tgtPorts[0] is None):
        print('[-] You must specify a target host and port[s].')
        exit(0)
    portScan(tgtHost, tgtPorts)


if __name__ == '__main__':
    main()
