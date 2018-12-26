import hashlib

db = {}


def get_md5(data):
    m = hashlib.md5()
    str = data.encode('utf-8')
    m.update(str)
    return m.hexdigest()


def register(username, password):
    db[username] = get_md5(password + username + 'padding')


def login(username, password):
    try:
        if db[username] == get_md5(password + username + 'padding'):
            print('login success!')
        else:
            print('login failed!')
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    register('test','abcde')
    print(db)
    login('test','abcde')  
