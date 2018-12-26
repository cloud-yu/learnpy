from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select

url = r'http://fhnw.fiberhome.com'

# firefox 驱动调用配置，并初始化一个firefox的webdriver实例
firefoxdriver = r'D:\Program Files\Mozilla Firefox\firefox.exe'
firebin = FirefoxBinary(firefoxdriver)
driver = webdriver.Firefox(firefox_binary=firebin, log_path=None)
driver.implicitly_wait(5)

# 使用phantomJS可以实现无界面调用
# driver = webdriver.PhantomJS()
driver.get(url)

element = driver.find_element_by_id(r'CCM_LoginMain1_txtUserNamelogin')
element.clear()
element.send_keys(r'username')

element = driver.find_element_by_id(r'CCM_LoginMain1_txtPasswordlogin')
element.clear()
element.send_keys(r'password')

element = driver.find_element_by_id(r'CCM_LoginMain1_ImageButtonlogin1')
element.click()

savedCookies = driver.get_cookies()

# driver = webdriver.Firefox(firefox_binary=firebin)
# driver.get(r'http://fhnw.fiberhome.com/overtime/OvertimeList.aspx')
# driver.delete_all_cookies()
# for cookie in savedCookies:
#     driver.add_cookie(cookie)
driver.get(r'http://fhnw.fiberhome.com/overtime/OvertimeEdit.aspx?type=1')

# 加班开始时间
select = Select(driver.find_element_by_id('DropDownList1'))
select.select_by_value(r'17:30')
# 加班结束时间
select = Select(driver.find_element_by_id('DropDownList2'))
select.select_by_value(r'21:30')

select = Select(driver.find_element_by_id('dlType'))
# select.select_by_visible_text('项目')
# index: 0 -- 部门；1 -- 项目
select.select_by_index(0)

select = Select(driver.find_element_by_id('dlArea'))
# 6008D---集成测试部；6007J---650接入PTN LMT
select.select_by_value('6007J')
# select.select_by_value('6008D')

element = driver.find_element_by_id('tbBZ')
element.clear()
# element.send_keys("650接入LMT加班")
element.send_keys("新员工答辩")

# element = driver.find_element_by_id('lbSave')
# element.click()

# element = driver.find_element_by_link('提交')
# element.click()
# driver.close()
