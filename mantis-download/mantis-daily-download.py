import requests
import xlwings
import os

url = r'http://fhnwmantis.fiberhome.com.cn/mantis'
login_url = url + r'/login.php'
select_pro_url = url + r'/set_project.php'
view_all_bug_url = url + r'/view_all_bug_page.php'
excel_export_url = url + r'/excel_xml_export.php'

login_data = {"return": "index.php", "username": "yuyun", "password": "q*963."}

# project_id 任务ID，可从网页源码处获取。
# 要导出V3R1M3总mantis，包含集成和中试是使用如下字段
select_pro_data = {"top_id": "286", "project_id": "286;1768"}

# 仅导出V3R1M3集成mantis时，使用如下字段
# select_pro_data = {"top_id": "286", "project_id": "286;1768;1769"}

headers = {
    "Connection":
    "keep-alive",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/63.0.3239.132 Safari/537.36"
}


def downloadExcel(filename):
    s = requests.Session()
    try:
        s.get(url, headers=headers)
    except BaseException as e:
        print('[-]', e)
        return 0
    else:
        print('[+] login mantis page')
        s.post(login_url, headers=headers, data=login_data)

        s.post(select_pro_url, headers=headers, data=select_pro_data)

        s.get(view_all_bug_url)
        print('[+] begin download mantis excel...')
        r2 = s.get(excel_export_url)

        with open(filename, 'wb') as f:
            print('[+] Save download mantis excel...')
            f.write(r2.content)
        print('[+] Save complete!!')
        return 1


def filterExcel(srcfile, template, tgtfile):
    print('[+] Begin working with excel....')
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
        print(e)
    finally:
        app.quit()
        print('[+] Jobs Done!')


if __name__ == '__main__':
    curdir = os.path.dirname(__file__)
    srcfile = os.path.join(curdir, '650V3R1M3-daily-mantis.xls')
    tmplate = os.path.join(curdir, 'mantis-daily-template.xlsx')
    tgtfile = os.path.join(curdir, '650V3R1M3-mantis.xlsx')

    t = downloadExcel(srcfile)
    if t:
        filterExcel(srcfile, tmplate, tgtfile)
