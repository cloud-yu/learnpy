import re

reg = re.compile(r'%[0-9A-F]{2}|.')
reg1 = re.compile('[0-9a-zA-Z._-]')


def revert_bits_in_byte(charcode):
    # yapf:disable
    # return (
    #     ((byte & (0x01)) << 7) | ((byte & (0x02)) << 5) |
    #     ((byte & (0x04)) << 3) | ((byte & (0x08)) << 1) |
    #     ((byte & (0x10)) >> 1) | ((byte & (0x20)) >> 3) |
    #     ((byte & (0x40)) >> 5) | ((byte & (0x80)) >> 7)
    # )
    # yapf:enable
    return int('{:08b}'.format(charcode & 0xFF)[::-1], 2)
# yapf:enable


def decode_character(data, index):
    if (data is '+'):
        ret = ord(' ')
    elif (len(data) == 1):
        ret = ord(data)
    else:
        ret = int(data.strip('%'), 16)
    return chr(revert_bits_in_byte(ret ^ 0x35 ^ (index & 0xff)))


def encode_character(data, index):
    chrcode = chr(revert_bits_in_byte(ord(data)) ^ 0x35 ^ (index & 0xff))
    return encode_data(chrcode)


def encode_data(chrcode):
    '''
    >>> encode_data(' ')
    '+'
    >>> encode_data('.')
    '.'
    >>> encode_data('i')
    'i'
    >>> encode_data('I')
    'I'
    >>> encode_data(chr(255))
    '%FF'
    '''
    if chrcode is ' ':
        encode_data = '+'
    elif reg1.match(chrcode):
        encode_data = chrcode
    else:
        encode_data = '%' + '{:02X}'.format(ord(chrcode))
    return encode_data


def decrypt(cryptpwd):
    splitcrypt = reg.findall(cryptpwd)
    return ''.join(map(decode_character, splitcrypt, range(len(splitcrypt))))


def encrypt(text):
    return ''.join(map(encode_character, text, range(len(text))))


class Account:
    '''
    Acount password encryption/decryption test
    >>> a1 = Account('username', 'password')
    >>> a1.encrypt_pwd
    '%3B%B2%F9%F8%DF%C6%7D%14'
    >>> a1.username
    'username'
    >>> a2 = Account('username', '%3B%B2%F9%F8%DF%C6%7D%14', is_encrypted=True)
    >>> a2.passwd
    'password'
    >>> a3 = Account(123, '234')
    Traceback (most recent call last):
        ...
    AssertionError: username must be a string
    >>> a3 = Account('username', 123)
    Traceback (most recent call last):
        ...
    AssertionError: password must be a string
    '''

    def __init__(self, username, password, is_encrypted=False):
        assert isinstance(username, str), 'username must be a string'
        assert isinstance(password, str), 'password must be a string'
        self.username = username
        if is_encrypted:
            self.encrypt_pwd = password
            self.passwd = decrypt(self.encrypt_pwd)
        else:
            self.passwd = password
            self.encrypt_pwd = encrypt(self.passwd)


myAccount = Account('yuyun', 'fh0211004565')
if __name__ == '__main__':
    import doctest
    doctest.testmod()
