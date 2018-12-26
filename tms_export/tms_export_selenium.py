from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

driver = webdriver.Firefox(firefox_binary=firebin, log_path=None)
driver.implicitly_wait(5)

url = r'http://fhnwtms.fiberhome.com/login.php'
driver.get(url)
element = driver.find_el

driver.find_element_by_xpath()


def login(driver):
    locator = (By.ID, 'captcha_pic')
    WebDriverWait(driver, 30, 1).until(EC.presence_of_element_located(locator))

    driver.find
    # 用户名
    element = driver.find_element_by_name('tl_login')
    element.clear()
    element.send_keys(r'余昀')
    # 密码
    element = driver.find_element_by_name('tl_password')
    element.clear()
    element.send_keys('q*963.')

    element.submit()


EC.frame_to_be_available_and_switch_to_it('mainframe')


def select_project(driver, testproj, target):
    driver.switch_to.frame('titlebar')
    selector = Select(driver.find_element_by_name('testproject'))
    selector.select_by_visible_text(testproj)

    driver.switch_to.default_content()
    WebDriverWait(driver, 30, 1).until(EC.frame_to_be_available_and_switch_to_it('mainframe'))
    driver.switch_to.frame('mainframe')

    locator = (By.LINK_TEXT, r'浏览测试用例')
    element = WebDriverWait(driver, 30, 1).until(EC.presence_of_element_located(locator))
    element.click()

    WebDriverWait(driver, 30, 1).until(EC.frame_to_be_available_and_switch_to_it('treeframe'))
    # element = driver.find_element_by_xpath('//ul/li/ul/li/div/[contains(text(), "{}")]'.format(target))
