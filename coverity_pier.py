import os
from bs4 import BeautifulSoup as BS

docpath = r'E:\Users\yuyun\Desktop\workspace\TempJob\650'
files = os.listdir(docpath)

# namedict = {}
names = []
for i in files:

    filepath = os.path.join(docpath, i)
    print(filepath)
    with open(filepath, 'r', encoding='gbk') as fp:
        text = fp.read()
        bsobj = BS(text, 'html.parser')
        find = bsobj.find_all('tr')
        for j in find:
            tr = j.find_all('td')
            if len(tr) != 10:
                continue
            elif tr[-2].text == chr(8730):
                names.append(tr[-4].text)
            else:
                continue

    # namedict[filepath] = names
names = set(names)
print(names)
print(len(names))
