#!/usr/lib/python2.7
# -*-coding:UTF-8-*-

import time
import requests
import json
import re

headers = {
    'Referer': 'http://202.103.24.68:90/p/30247dd99271a6806206be0598a1cf9e/index.html?bmV3cy5iYWlkdS5jb20v',
    'Host': '202.103.24.68:90',
    'Connection': 'keep-alive',
}

data = {
    "uri": "bmV3cy5iYWlkdS5jb20v",
    "terminal": "pc",
    "login_type": "login",
    "check_passwd": "0",
    "show_tip": "block",
    "show_change_password": "none",
    "short_message": "none",
    "show_captcha": "none",
    "show_read": "block",
    "show_assure": "none",
    "username": "zhouquan2478",
    "assure_phone": "",
    "password1": "03260309zq",
    "password": "9%F8%7BZ%3D%FC%3F%AEc%B2",
    "new_password": "",
    "retype_newpassword": "",
    "captcha_value": "",
    "save_user": "1",
    "save_pass": "1",
    "read": "1"
}

s = requests.Session()
print "Try to connect to the Internet..."
# step1 通过请求百度，触发重定向到认证页面
r = s.get('http://www.baidu.com', allow_redirects=False)
if r.status_code == 302:
    url1 = r.headers['location']
else:
    r = s.get('http://news.baidu.com', allow_redirects=False)
    if r.status_code == 302:
        url1 = r.headers['location']
    else:
        url1 = "http://202.103.24.68:44567/login?uri=bmV3cy5iYWlkdS5jb20v"

time.sleep(2)

# step2 请求重定向页面
print "[DEBUG info]" + url1
r = s.get(url1, allow_redirects=False)
if r.status_code == 302:
    url2 = r.headers['location']
time.sleep(2)

# step3 再次请求重定向页面
print "[DEBUG info]" + url2
r = s.get(url2, allow_redirects=False)
time.sleep(2)

print "Jump to the authentication page..."
r = s.get("http://202.103.24.68:90/p/30247dd99271a6806206be0598a1cf9e/index.html", allow_redirects=False)
# r = s.post("http://202.103.24.68:90/p/30247dd99271a6806206be0598a1cf9e/index.html?bmV3cy5iYWlkdS5jb20v", headers=headers,data=data)
time.sleep(2)
print "Began to authenticate..."
r = s.post("http://202.103.24.68:90/login", headers=headers, data=data)
result = re.search(r'zhouquan2478', r.content)
if result is not None:
    print "Authentication Ok!"
else:
    print "Authentication failed!"
s.close()
