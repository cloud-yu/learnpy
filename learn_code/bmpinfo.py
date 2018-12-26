import struct


def isbmp(file):
    try:
        with open(file, 'rb') as f:
            b_head = f.read(30)
        head = struct.unpack('=ccIIIIIIHH', b_head)
        print(head)
        f_type = head[0].decode() + head[1].decode()
        if f_type == 'BM':
            print('%s is a bmp file' % file)
            print('size of bmp: %d' % head[2])
            print('size: %d x %d' % (head[6], head[7]))
            print('color: %d' % head[-1])
        else:
            print('%s is not a bmp file' % file)

    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    isbmp('test.bmp')
