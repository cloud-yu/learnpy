import requests
import re
from bs4 import BeautifulSoup as BS
import os
import codecs
import xml.etree.ElementTree as ET
import xml.dom.minidom
import json

url = r'http://fhnwtms.fiberhome.com/login.php'
testprojurl = r'http://fhnwtms.fiberhome.com/lib/general/navBar.php'

login_data = {"tl_login": "余昀", "tl_password": "q*963."}

headers = {
    "Connection":
    "keep-alive",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/63.0.3239.132 Safari/537.36"
}

reg = re.compile(r'\((\d+)\)$')


class TmsExport():

    def __init__(self):
        self.s = requests.Session()

    def loginAndGettestprojlist(self):
        self.s.post(url, headers=headers, data=login_data)
        res = self.s.get(testprojurl)
        res.encoding = 'utf-8'
        result = re.search(r'余昀', res.text)
        if result is not None:
            print('Login Ok!')
            bsobj = BS(res.text, 'html.parser')
            findselector = bsobj.find('select', {'name': 'testproject'})
            options = findselector.find_all('option')

            for i in options:
                print('id: %-15s \t title: %s' % (i.get('value'), i.get('title')))
            return options

        else:
            print('Login Failed!')

    def gettestcasesummary(self, root_node, node, printable=False):
        testtree = r'http://fhnwtms.fiberhome.com/lib/ajax/gettprojectnodes.php'
        data1 = {'root_node': str(root_node), 'node': str(node)}
        resp = self.s.post(testtree, data=data1)
        if resp.content.startswith(codecs.BOM_UTF8):
            resp.encoding = 'utf-8-sig'
        else:
            resp.encoding = 'utf8'
        if printable:
            for i in resp.json():
                print('id: %-15s \t title: %s' % (i.get('id'), i.get('testlink_node_name')))
        return resp.json()

    def gettestcase(self, root_node, node):
        casesum = self.gettestcasesummary(root_node, node)
        res = []
        if isinstance(casesum, list):
            for i in casesum:
                #     num = reg.search(i['text'])
                #     if num and num.group(1) == '0':
                #         pass
                #     else:
                testinfo = {}
                testinfo['type'] = i['testlink_node_type']
                testinfo['id'] = i['id']
                if testinfo['type'] == 'testsuite':
                    testinfo['name'] = i['testlink_node_name']
                    if reg.search(i['text']).group(1) == '0':
                        continue
                    else:
                        testinfo['nexthop'] = self.gettestcase(root_node, testinfo['id'])
                elif testinfo['type'] == 'testcase':
                    testinfo['name'] = i['text']
                res.append(testinfo)
            return res


def createNode1(parent, data):

    if data['type'] == 'testcase':
        nodename = ET.SubElement(parent, 'testcase')
        nodename.text = data['name']

    if data['type'] == 'testsuite':
        nodename = ET.SubElement(parent, 'title', {'title': data['name']})

        for i in data['nexthop']:
            createNode1(nodename, i)


def createNode(data):
    # nodename2 = doc.createElement('testcase')
    # nodename2.appendChild(doc.createTextNode(''))
    # lasttype = 'suite'

    if data['type'] == 'testcase':
        nodename = doc.createElement('testcase')
        nodename.appendChild(doc.createTextNode(data['name']))
        # lasttype = 'case'
    if data['type'] == 'testsuite':
        nodename = doc.createElement('title')
        nodename.setAttribute('title', data['name'])
        # lasttype = 'suite'
        # blanknode = doc.createElement('testcase')
        # blanknode.appendChild(doc.createTextNode(''))
        # nodename.appendChild(blanknode)
        for i in data['nexthop']:
            nodename.appendChild(createNode(i))
            # nodename.appendChild(nodename2)

    return nodename


if __name__ == '__main__':
    t = TmsExport()
    print('choose a testproject:')
    t.loginAndGettestprojlist()
    # root_id = input('\r\nchoose the testproject id: ')
    root_id = '699389'
    t.gettestcasesummary(root_id, root_id)
    res = t.gettestcase(root_id, '888004')
    # 保存res结果到test.json
    # with open(r'f:\test.json', 'w', encoding='utf8') as f:
    #     json.dump(res, f, ensure_ascii=False)

    # # 从test.json读取数据生成xml
    # with open(r'f:\test.json', 'r', encoding='utf-8') as fp:
    #     res = json.load(fp)

    # a = ET.Element('root')
    # for i in res:
    #     createNode1(a, i)
    # tree = ET.ElementTree(a)
    # tree.write(r'f:\tree.xml', encoding='utf-8')

    doc = xml.dom.minidom.Document()
    root = doc.createElement('root')
    for i in res:
        root.appendChild(createNode(i))

    res1 = t.gettestcase(root_id, '1316047')
    for i in res1:
        root.appendChild(createNode(i))

    doc.appendChild(root)
    with open(r'F:\xxx2.xml', 'w', encoding="utf-8") as fp:
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="UTF-8")
