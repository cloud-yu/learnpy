import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urljoin
import re
import xlwings
import logging
import os
import sys
sys.path.append(r'f:\temp_py')
from baidu_ocr import Ocr  # noqa: E402
# 定义日志记录器
logger = logging.getLogger()
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)
#################

loginurl = r'http://sso.fiberhome.com/cas-fiberhome/login'
mantislogin = r'http://fhnwmantis.fiberhome.com/mantis/login.php'
headers = {
    "Connection":
    "keep-alive",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/71.0.3578.98 Safari/537.36"
}
url = r'http://fhnwmantis.fiberhome.com/mantis'
select_pro_url = url + r'/set_project.php'
view_all_bug_url = url + r'/view_all_bug_page.php'
excel_export_url = url + r'/excel_xml_export.php'

# project_id 任务ID，可从网页源码处获取。
# 要导出V3R1M3总mantis，包含集成和中试是使用如下字段
select_pro_data = {"top_id": "286", "project_id": "286;1768"}

# 仅导出V3R1M3集成mantis时，使用如下字段
# select_pro_data = {"top_id": "286", "project_id": "286;1768;1769"}
# mainpagedata = {'MANTIS_secure_session': '0'}
s = requests.session()


def loginPage():
    global s
    t = Ocr()
    flag = True
    while flag:
        try:
            req1 = s.get(loginurl, headers=headers)  # req1.status_code == 200
            assert req1.status_code == 200, 'status_code %s' % req1.status_code
            bsobj = BS(req1.text, 'html.parser')
            find = bsobj.find('input', {'id': 'captcha', 'name': 'captcha'}).next_sibling.get('src')
            captchaurl = urljoin(req1.url, find)
            logger.info('captchaurl is %s' % captchaurl)

            req2 = s.get(captchaurl, headers=headers)

            with open(r'captcha.jpg', 'wb') as fp:
                fp.write(req2.content)

            t.get_Fileresult(r'captcha.jpg')
            captcha = t.result_strings()
            assert len(captcha) == 4, 'captcha failed'
            logger.info(captcha)
            flag = False
        except AssertionError as res:
            logger.error('[-] %s' % res)
            logger.error('[!] repeat login...')
    logindata = {'username': 'yuyun', 'password': 'qaz!12345', 'captcha': captcha, 'locale': "zh_CN"}
    res = bsobj.find('section', {'class': 'row btn-row'}).find_all('input', {'type': 'hidden'})
    for i in res:
        logindata[i.get('name')] = i.get('value')

    s.post(loginurl, headers=headers, data=logindata)
    req3 = s.post(mantislogin, headers=headers, data=logindata)
    result = re.search(r'yuyun', req3.text)
    if result:
        logger.info('[+] login successful!!')
        return True
    else:
        logger.error('[-] login failed!')
        return False


def downloadExcel(filename):
    global s
    s.post(select_pro_url, headers=headers, data=select_pro_data)
    s.get(view_all_bug_url)
    logger.info('[+] begin download mantis excel...')
    r2 = s.get(excel_export_url)
    with open(filename, 'wb') as f:
        logger.info('[+] Save download mantis excel...')
        f.write(r2.content)
    logger.info('[+] Save complete!!')
    return 1


def filterExcel(srcfile, template, tgtfile):
    logger.info('[+] Begin working with excel....')
    # 创建一个app对象，连接到excel程序
    app = xlwings.App(visible=False, add_book=False)
    # 关闭excel打开兼容性文件时的提示信息
    app.display_alerts = False
    # 打开源excel与目的excel
    srcwb = app.books.open(srcfile)
    tmpwb = app.books.open(template)
    try:
        # 获取源excel有效区间的range对象
        srng = srcwb.sheets(1).range('A1').expand()
        # 获取有效区间的tuple(row,column)
        shape = srng.shape
        tmpwb.sheets(1).clear()
        tmpwb.sheets(1).range((1, 1)).value = srng.value
        sht = tmpwb.sheets(2)
        # sht.activate()
        # row = shape[0]
        if tmpwb.sheets(1).range('A1').expand().rows.count > 2:
            sht.range('A3').expand().clear_contents()
            trng = sht.range('A1').expand()
            column = min(trng.shape[1], shape[1])
            # 将模板中第二行中每一列的公式向下复制，直到行数与第一页内容相同(各单元格格式由模板决定)
            for i in range(1, column + 1):
                sht.range((3, i), (shape[0], i)).formula = sht.range((2, i)).formula

        # 为方便后续处理表格内容（表格2中实际内容为公式，需要将文本单独拷贝出来），将表格2文本复制到tgtfile
        if os.path.exists(tgtfile):
            tgtwb = app.books.open(tgtfile)
            tgtwb.sheets(1).api.AutoFilter.ShowAllData()  # 清除筛选
            tgtwb.sheets(1).clear()
        else:
            tgtwb = app.books.add()

        trng = sht.range('A1').expand()
        tgtwb.sheets(1).range((1, 1)).value = trng.value
        # 将模板中报告日期的单元格格式设置为‘yyyy/m/d'的格式。范围range((2,4),(shape[0],4))
        tgtwb.sheets(1).range((2, 4), (shape[0], 4)).number_format = 'yyyy/m/d'
        # 设置筛选为 状态中不包含 “中试”，”集成“字样的项
        tgtwb.sheets(1).api.UsedRange.AutoFilter(
            Field=6,
            Criteria1="<>*集成*",
            Operator=xlwings.constants.AutoFilterOperator.xlAnd,
            Criteria2="<>*中试*")

        tgtwb.save(tgtfile)
        srcwb.close()
        tmpwb.close()
        tgtwb.close()
    except BaseException as e:
        logger.error(e)
    finally:
        app.quit()
        logger.info('[+] Jobs Done!')


if __name__ == '__main__':
    curdir = os.path.dirname(__file__)
    srcfile = os.path.join(curdir, '650V3R1M3-daily-mantis.xls')
    tmplate = os.path.join(curdir, 'mantis-daily-template.xlsx')
    tgtfile = os.path.join(curdir, '650V3R1M3-mantis.xlsx')

    t = loginPage()
    if t:
        downloadExcel(srcfile)
        filterExcel(srcfile, tmplate, tgtfile)
