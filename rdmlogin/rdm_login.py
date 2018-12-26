import pytesseract
import io
# import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.chrome.options import Options
from PIL import Image
import json
import datetime as dt
import calendar
import os
import logging
import sys
sys.path.append(r'f:\temp_py')
from baidu_ocr import Ocr  # noqa: E402

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# 实例化日志记录器，并配置格式
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)


def login(driver):
    # 创建一个OCR实例
    t = Ocr()
    locator = (By.XPATH, '//section/p/input[@id="captcha"]/../img')
    WebDriverWait(driver, 30, 1).until(EC.presence_of_element_located(locator))
    driver.fullscreen_window()
    piclocate = driver.find_element(*locator).rect
    # 设定剪裁窗口大小
    box = (piclocate.get('x'), piclocate.get('y'), piclocate.get('x') + piclocate.get('width'),
           piclocate.get('y') + piclocate.get('height'))
    # 创建一个二进制IO存放当前屏幕截图
    fp = io.BytesIO(driver.get_screenshot_as_png())
    im = Image.open(fp)
    # 剪裁截图并转为灰度图片方便识别
    im = im.crop(box).convert('L')

    # 保存灰度图像后调用baidu-ocr识别验证码
    im.save(r'captcha.jpg')
    t.get_Fileresult(r'captcha.jpg', accur=True)
    codetext = t.result_strings()

    # 图片识别
    # codetext = pytesseract.image_to_string(im).strip('\n')

    logger.info(codetext)
    # 用户名
    element = driver.find_element_by_id('username')
    element.clear()
    # element.send_keys('xhchen5865')
    element.send_keys('yuyun')
    # 密码
    element = driver.find_element_by_id('password')
    element.clear()
    # element.send_keys('fh0211005865')
    element.send_keys('qaz!12345')
    # 验证码
    logger.info('codetext: %s' % codetext)
    element = driver.find_element_by_id('captcha')
    element.clear()
    element.send_keys(codetext)
    # 登录
    for i in range(3):
        try:
            element = driver.find_element_by_id('btn-submit')
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            break
        except Exception as e:
            logger.error("[x] click exception for the %d times: %s" % (i + 1, e))

    return im, codetext


def select_task(driver, taskid):
    driver.switch_to.default_content()
    logger.info('switch to default frame')
    WebDriverWait(driver, 30, 1).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'main')))
    logger.info('switch to main frame')
    # element = driver.find_element_by_id(taskid)
    locator = (By.XPATH, '//tr[@id="{}"]/td[8]/div/span/a'.format(taskid))
    try:
        logger.info('choose task')
        WebDriverWait(driver, 30, 1).until(EC.element_to_be_clickable(locator), 'Timeout!!!')
    except TimeoutException as e:
        logger.error('[x] can not find the clickable element: ', format(e))
        raise e
    except Exception as e:
        logger.error('[x] can not find the clickable element!\n', format(e))
        logger.error('[*] relocate the element')

    element = driver.find_element(*locator)
    for i in range(3):
        try:

            # driver.execute_script("arguments[0].scrollIntoView();", element)
            # element.click()
            ActionChains(driver).move_to_element(element).click().perform()

            break
        except Exception as e:
            logger.error('[x] click exception for the %d times: %s' % (i + 1, e))

    # print('select done')
    driver.switch_to_default_content()
    # print('switch to top frame')


def fill_tasklog(driver, content):

    driver.switch_to.frame('main')
    driver.switch_to.frame('taskPage')
    driver.switch_to.frame('baseInfoFrm')
    # print('begin to find img')
    WebDriverWait(driver, 30, 1).until(
        EC.element_to_be_clickable((By.XPATH, '//li[@field="report_action_date"]/div[2]/img')))
    # print('img find')
    # 处理时间参数
    cal = calendar.Calendar()
    today = dt.datetime.now().date()
    thismonthcal = list(cal.itermonthdates(today.year, today.month))
    tgtdate = dt.date(*list(map(int, content['date'].split('-'))))
    if tgtdate != today:
        locator = (By.XPATH, '//div[@id="c_calendarDiv"]')

        # selenium的actionchain可能click操作没有响应
        for i in range(3):
            try:
                logger.warn('[%d]locate the element...' % i)
                element = driver.find_element_by_xpath('//li[@field="report_action_date"]/div[2]/img')
                ActionChains(driver).move_to_element(element).click().perform()
                # driver.execute_script("arguments[0].scrollIntoView();", element)
                # element.click()
                WebDriverWait(driver, 5, 1).until(EC.visibility_of_element_located(locator), 'Timeout!!!')
                break
            except Exception as e:
                logger.error("[x] click exception:", format(e))
        # ActionChains(driver).move_to_element(element).click().perform()
        # WebDriverWait(driver, 30, 1).until(EC.visibility_of_element_located(locator))
        # print('calendar find')
        element = driver.find_element_by_xpath('//div[@id="c_calendarDiv"]')

        # 判断目标日期是否在本月月历中，如果是，直接点击天数即可
        if tgtdate in thismonthcal:
            logger.info('same month,just choose days')
        # 年份不相等则切换年份
        elif tgtdate.year != today.year:
            element.find_element_by_xpath('./div/span[@id="c_year"]').click()
            # ActionChains(driver).move_to_element(element).click().perform()
            Select(element.find_element_by_id(
                r'c_selectYear')).select_by_visible_text('{}'.format(tgtdate.year))  # yapf: disable
        # 月份不相等则切换月份
        elif tgtdate.month != today.month:
            element.find_element_by_xpath('./div/span[@id="c_month"]').click()
            # ActionChains(driver).move_to_element(element).click().perform()
            Select(element.find_element_by_id(
                r'c_selectMonth')).select_by_visible_text('{}'.format(tgtdate.month))  # yapf: disable
        # yapf: disable
        element.find_element_by_xpath(
            '//div[@id="c_calendarDiv"]/table/tbody/tr/td[@title="{}"]'.format(content['date'])).click()
        # yapf: enable

    # 填写完成率
    element = driver.find_element_by_xpath('//*[@id="report_rate"]')
    element.clear()
    element.send_keys(content['rate'])
    # 填当日工作量
    element = driver.find_element_by_xpath('//*[@id="report_in_work"]')
    element.clear()
    element.send_keys(content['workload'])
    # 填当日工作内容
    element = driver.find_element_by_xpath('//*[@id="operate_remark"]')
    element.clear()
    element.send_keys(content['describe'])

    # 提交
    driver.switch_to.parent_frame()
    driver.find_element_by_xpath('//div[@id="operateDiv"]/input[1]').click()
    driver.switch_to_default_content()
    driver.find_element_by_xpath(
        '//div[@id="dialogPanel"]/div[@class="dialog-body"]/table/tbody/tr/td[2]/input[1]').click()


def process(tasklist):
    driver = webdriver.Firefox(firefox_binary=firebin, log_path=None)
    driver.implicitly_wait(5)
    driver.get(url)
    try:
        login(driver)
        for i in tasklist:
            logger.info('fill date: %s' % i['taskdiary']['date'])
            select_task(driver, i['taskid'])
            fill_tasklog(driver, i['taskdiary'])
    except Exception as e:
        logger.error(e)
    finally:
        driver.quit()


if __name__ == '__main__':
    url = r'http://rdmprd.fiberhome.com.cn/main.do'
    firefoxdriver = r'D:\Program Files\Mozilla Firefox\firefox.exe'
    firebin = FirefoxBinary(firefoxdriver)
    jsfilepath = os.path.join(os.path.split(os.path.realpath(__file__))[0], r'rdmtask.json')
    with open(jsfilepath, 'r', encoding='utf-8') as fp:
        data = json.load(fp)

    tasknum = len(data)
    tasklist = []
    for i in range(tasknum):
        for j in range(len(data[i]['taskdiary'])):
            tasklist.append({'taskid': data[i]['taskid'], 'taskdiary': data[i]['taskdiary'][j]})
    process(tasklist)
