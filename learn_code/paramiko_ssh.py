import paramiko
import optparse


class pyssh():

    def __init__(self):
        self.sname = paramiko.SSHClient()
        self.sname.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self, hostname, port, username, password):
        self.sname.connect(hostname, port, username, password)
        return self.sname

    def send(self, cmd, *args):
        stdin, stdout, stderr = self.sname.exec_command(cmd, *args)
        return (stdout.read().decode('utf-8'), stderr.read().decode('utf-8'))

    def close(self):
        self.sname.close()
        return self.sname


def main():
    parser = optparse.OptionParser(
        "usage: %prog -H <host> -p <port> -U <username> -P <password>")
    parser.add_option(
        '-H',
        '--hostname',
        dest='host',
        type='string',
        help='specify connect host')
    parser.add_option(
        '-p', '--port', dest='port', type='int', help='specify connect port')
    parser.add_option(
        '-U',
        '--username',
        dest='username',
        type='string',
        help='specify username')
    parser.add_option(
        '-P',
        '--password',
        dest='password',
        type='string',
        help='specify password')
    (options, args) = parser.parse_args()
    host = options.host
    port = options.port
    username = options.username
    password = options.password
    s = pyssh()
    s.connect(host, port, username, password)
    print(s.send('cat /proc/version')[0])
    # print(s.send('ls -la /mnt/userdir')[0])
    s.close()


if __name__ == '__main__':
    main()
