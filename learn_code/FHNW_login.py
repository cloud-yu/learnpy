#!env python
# -*- coding: UTF-8 -*-
import requests
# from bs4 import BeautifulSoup as bs
header = {
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':
    'gzip, deflate',
    'Accept-Language':
    'zh-CN,zh;q=0.9',
    'Cache-Control':
    'max-age=0',
    'Content-Length':
    '14019',
    'Content-Type':
    'application/x-www-form-urlencoded',
    'DNT':
    '1',
    'Host':
    'fhnw.fiberhome.com',
    'Origin':
    'http://fhnw.fiberhome.com',
    'Proxy-Connection':
    'keep-alive',
    'Referer':
    'http://fhnw.fiberhome.com/',
    'Upgrade-Insecure-Requests':
    '1',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

info = {
    '__LASTFOCUS':
    '',
    '__EVENTTARGET':
    '',
    '__EVENTARGUMENT':
    '',
    '__VIEWSTATE':
    '/wEPDwUKMTI1NzcwNTI5Nw9kFgICAQ9kFhBmD2QWAmYPDxYCHgRUZXh0BdcPJm5ic3A7Jm5ic3A7PGEgaHJlZj0namF2YXNjcmlwdDp2YXJ3aW49d2luZG93Lm9wZW4oImh0dHA6Ly9maG53LmZpYmVyaG9tZS5jb20vU3lzdGVtL2FmZmljaGVWaWV3LmFzcHg/aWQ9MjIiLG51bGwsIndpZHRoPTYwMCxoZWlnaHQ9NjM5LHNjcm9sbGJhcnM9eWVzIik7aGlzdG9yeS5mb3J3YXJkKCk7Jz48c3BhbiBjbGFzcz3otoXpk77mjqUzPueDveeBq+mAmuS/oee7vOWQiOmDqOiwg+aLqOS4juebmOeCueezu+e7n+eUqOaIt+aJi+WGjDwvc3Bhbj48L2E+Jm5ic3A7Jm5ic3A7Jm5ic3A7Jm5ic3A7PGEgaHJlZj0namF2YXNjcmlwdDp2YXJ3aW49d2luZG93Lm9wZW4oImh0dHA6Ly9maG53LmZpYmVyaG9tZS5jb20vU3lzdGVtL2FmZmljaGVWaWV3LmFzcHg/aWQ9MTkiLG51bGwsIndpZHRoPTYwMCxoZWlnaHQ9NjM5LHNjcm9sbGJhcnM9eWVzIik7aGlzdG9yeS5mb3J3YXJkKCk7Jz48c3BhbiBjbGFzcz3otoXpk77mjqUzPuWbuuWumui1hOS6p+euoeeQhuW3peS9nOaWh+ahozwvc3Bhbj48L2E+Jm5ic3A7Jm5ic3A7Jm5ic3A7Jm5ic3A7PGEgaHJlZj0namF2YXNjcmlwdDp2YXJ3aW49d2luZG93Lm9wZW4oImh0dHA6Ly9maG53LmZpYmVyaG9tZS5jb20vU3lzdGVtL2FmZmljaGVWaWV3LmFzcHg/aWQ9MjEiLG51bGwsIndpZHRoPTYwMCxoZWlnaHQ9NjM5LHNjcm9sbGJhcnM9eWVzIik7aGlzdG9yeS5mb3J3YXJkKCk7Jz48c3BhbiBjbGFzcz3otoXpk77mjqUzPueJqeaWmemHh+i0reS/oeaBrzwvc3Bhbj48L2E+Jm5ic3A7Jm5ic3A7Jm5ic3A7Jm5ic3A7PGEgaHJlZj0namF2YXNjcmlwdDp2YXJ3aW49d2luZG93Lm9wZW4oImh0dHA6Ly9maG53LmZpYmVyaG9tZS5jb20vU3lzdGVtL2FmZmljaGVWaWV3LmFzcHg/aWQ9MTgiLG51bGwsIndpZHRoPTYwMCxoZWlnaHQ9NjM5LHNjcm9sbGJhcnM9eWVzIik7aGlzdG9yeS5mb3J3YXJkKCk7Jz48c3BhbiBjbGFzcz3otoXpk77mjqUzPuWboOWFrOWHuuWbve+8muOAiuWHuuWig+ivgeaYjuOAi+OAgeetvuivgeWPiuS/nemZqeebuOWFs+S6i+WunDwvc3Bhbj48L2E+Jm5ic3A7Jm5ic3A7Jm5ic3A7Jm5ic3A7PGEgaHJlZj0namF2YXNjcmlwdDp2YXJ3aW49d2luZG93Lm9wZW4oImh0dHA6Ly9maG53LmZpYmVyaG9tZS5jb20vU3lzdGVtL2FmZmljaGVWaWV3LmFzcHg/aWQ9MTciLG51bGwsIndpZHRoPTYwMCxoZWlnaHQ9NjM5LHNjcm9sbGJhcnM9eWVzIik7aGlzdG9yeS5mb3J3YXJkKCk7Jz48c3BhbiBjbGFzcz3otoXpk77mjqUzPuihjOaUv+ebuOWFs+W3peS9nOa1geeoi+WPiuinhOiMgzwvc3Bhbj48L2E+Jm5ic3A7Jm5ic3A7Jm5ic3A7Jm5ic3A7PGEgaHJlZj0namF2YXNjcmlwdDp2YXJ3aW49d2luZG93Lm9wZW4oImh0dHA6Ly9maG53LmZpYmVyaG9tZS5jb20vU3lzdGVtL2FmZmljaGVWaWV3LmFzcHg/aWQ9MjAiLG51bGwsIndpZHRoPTYwMCxoZWlnaHQ9NjM5LHNjcm9sbGJhcnM9eWVzIik7aGlzdG9yeS5mb3J3YXJkKCk7Jz48c3BhbiBjbGFzcz3otoXpk77mjqUzPuWKnuS6i+aMh+WNlzwvc3Bhbj48L2E+Jm5ic3A7Jm5ic3A7Jm5ic3A7Jm5ic3A7PGEgaHJlZj0namF2YXNjcmlwdDp2YXJ3aW49d2luZG93Lm9wZW4oImh0dHA6Ly9maG53LmZpYmVyaG9tZS5jb20vU3lzdGVtL2FmZmljaGVWaWV3LmFzcHg/aWQ9MTYiLG51bGwsIndpZHRoPTYwMCxoZWlnaHQ9NjM5LHNjcm9sbGJhcnM9eWVzIik7aGlzdG9yeS5mb3J3YXJkKCk7Jz48c3BhbiBjbGFzcz3otoXpk77mjqUzPueglOWPkea1geeoi+afpeeci+ivtOaYjjwvc3Bhbj48L2E+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',
    '__EVENTVALIDATION':
    '/wEWCgLAztnGAgL2hcDlDQKP9dDICAKulKyEDQKxlKyEDQK3lKyEDQKQx4zODwLnsZXtCgLVtaiXDALSvKi+DE0LAiLm9v1HNlP4lVY0CqHTChKe',
    'CCM_LoginMain1$txtUserNamelogin':
    'yuyun',
    'CCM_LoginMain1$txtPasswordlogin':
    '0211004565',
    'CCM_LoginMain1$ddAutoLogin':
    '365',
    'CCM_LoginMain1$ImageButtonlogin1.x':
    '11',
    'CCM_LoginMain1$ImageButtonlogin1.y':
    '5',
    'tbSearch':
    '',
}

s = requests.Session()
# s.get(r'http://fhnw.fiberhome.com')
s.post(r'http://fhnw.fiberhome.com/Default.aspx', headers=header, data=info, allow_redirects=False, timeout=3)
cookies = s.cookies
r = s.get(r'http://fhnw.fiberhome.com', cookies=cookies)