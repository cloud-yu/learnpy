from urllib import request
from urllib import parse
import re
import time
import logging
import logging.handlers

# # 初始化logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(filename)s %(levelname)s %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S',
#     filename=r'E:\Auth.log',
#     filemode='a+')

# 初始化一个logger实例
logger = logging.getLogger('login')
logger.setLevel(logging.INFO)
# 定义一个handler
handler = logging.handlers.RotatingFileHandler(r'E:\Auth.log', 'a+',
                                               20 * 1024 * 1024, 3)

# 给日志定义一个formatter
fmt = logging.Formatter('%(asctime)s %(filename)s %(levelname)s %(message)s')
# 给handler设置formatter
handler.setFormatter(fmt)
logger.addHandler(handler)

# 初始化登陆数据
info = {
    'username': 'yuyun',
    'password': '%BB%B2i%B2%BD%7C%FF%1E%91',
    'login_type': 'login'
}
url = r'http://202.103.24.68:90/login'


def login():

    data = parse.urlencode(info).encode('utf-8')
    req = request.Request(url, data=data, headers={})
    resp = request.urlopen(req)
    resp_data = resp.read().decode('utf-8')
    result = re.search('成功登录', resp_data)
    if result:
        # logger.info(result.group())
        return 0
    else:
        # logger.info('login failed!')
        return 1


uri0 = r'http://www.baidu.com'

while True:
    try:
        checklink = request.urlopen(uri0).geturl()
        if re.search(r'202.103.24.68:90', checklink):
            while login():
                logger.info('[*] login failed! retry after 3s.')
                time.sleep(3)
            logger.info('[+] login successfully! sleep 30min.')
            time.sleep(1800)
        else:
            logger.info('[+] connection works well, sleep 30min.')
            time.sleep(1800)
    except Exception as e:
        logger.error('[!] %s' % e)
        logger.info('[-] unexpected error occured, retry after 10min.')
        time.sleep(600)