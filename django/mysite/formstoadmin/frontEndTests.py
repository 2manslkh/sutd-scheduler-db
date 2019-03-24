from selenium import webdriver
from applitools.eyes import Eyes
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
# only used when I'm using certain EC; else I don't find it faster

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select
# normally used for <select> items but can't be used here somehow.
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import random
import logging
import time
import datetime


formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


logger = setup_logger('info_level_logger', 'formsINFO.log')

start = time.time()
now = datetime.datetime.now()
s = now.strftime("%d %B %Y, %H:%M:%S")
logger.info("Test ran on: {} at{}".format(s.split(',')[0], s.split(',')[1]))
driver = webdriver.Chrome(r"C:\Users\Tea\Desktop\50.003 Event Scheduler\sutd-scheduler-db\django\chromedriver_win32 (1)\chromedriver.exe")


class FrontEndTests:

    eyes = Eyes()

    # Initialize the eyes SDK and set your private API key.
    eyes.api_key = 'IlUcgRAO105BlmoORdtUxbK8CUKg3KRSa8q4f3iACoY1I110'

    try:
        # Start the test and set the browser's viewport size to 800x600.
        eyes.open(driver=driver, app_name='Hello World!', test_name='eventScheduler')
        # Navigate the browser to the "hello world!" web-site.
        driver.get('http://localhost:8000/')

        driver.set_window_size(1536, 673)
        driver.set_window_position(0, 0)

        eyes.check_window('Login')

        driver.find_element_by_xpath("//a[text()='Home']").click()
        eyes.check_window('Redirected to login')

        # show dropdown menu
        driver.find_element_by_xpath("//a[contains(text(),'Forms')]").click()
        eyes.check_window('Dropdown menu')

        driver.find_element_by_xpath("//a[contains(text(),'Schedule R')]").click()
        eyes.check_window('Redirected to login')

        assert(driver.current_url == "http://localhost:8000/login/?next=/requestform/")

        # test registeration

        RANDOM_NAME = "100000"
        LEGAL_PASSWORD = 'SomeStrongPW09!'
        WEAK_PASSWORD = 'someweakpassword'

        ran_num = random.randint(1001, 5000)
        ran_num_str = str(ran_num)
        ran_name = "100" + ran_num_str
        Email = ran_name + '@mymail.sutd.edu.sg'

        driver.find_element_by_xpath("//a[text()='Register']").click()
        eyes.check_window('Registration page')

        username = driver.find_element_by_xpath('//input[@name="username"]')
        username.send_keys(ran_name)

        email = driver.find_element_by_xpath('//input[@name="email"]').click()
        eyes.check_window('Focused textbox')
        driver.find_element_by_xpath('//input[@name="email"]').send_keys(Email)

        pw1 = driver.find_element_by_xpath('//input[@name="password1"]')
        pw1.send_keys(LEGAL_PASSWORD)
        pw2 = driver.find_element_by_xpath('//input[@name="password2"]')
        pw2.send_keys(LEGAL_PASSWORD)
        pw2.send_keys(Keys.RETURN)

        eyes.check_window("Submitted")

        # re-registering with the same username
        driver.find_element_by_xpath("//a[text()='Register']").click()

        username = driver.find_element_by_xpath('//input[@name="username"]')
        username.send_keys(ran_name)

        email = driver.find_element_by_xpath('//input[@name="email"]').click()
        driver.find_element_by_xpath('//input[@name="email"]').send_keys(Email)

        pw1 = driver.find_element_by_xpath('//input[@name="password1"]')
        pw1.send_keys(LEGAL_PASSWORD)
        pw2 = driver.find_element_by_xpath('//input[@name="password2"]')
        pw2.send_keys(LEGAL_PASSWORD)
        pw2.send_keys(Keys.RETURN)

        assert('A user with that username already exists.' in driver.page_source)
        eyes.check_window("same user error message")

        driver.find_element_by_xpath("//a[text()='Register']").click()

        # test weakpasswords
        username = driver.find_element_by_xpath('//input[@name="username"]')
        username.send_keys(RANDOM_NAME)

        email = driver.find_element_by_xpath('//input[@name="email"]').click()
        driver.find_element_by_xpath('//input[@name="email"]').send_keys(Email)

        pw1 = driver.find_element_by_xpath('//input[@name="password1"]')
        pw1.send_keys(WEAK_PASSWORD)
        pw2 = driver.find_element_by_xpath('//input[@name="password2"]')
        pw2.send_keys(WEAK_PASSWORD)
        pw2.send_keys(Keys.RETURN)

        driver.find_element_by_xpath("//a[text()='Register']").click()
        username = driver.find_element_by_xpath('//input[@name="username"]')
        username.send_keys(RANDOM_NAME)

        email = driver.find_element_by_xpath('//input[@name="email"]').click()
        driver.find_element_by_xpath('//input[@name="email"]').send_keys(Email)
        pw1 = driver.find_element_by_xpath('//input[@name="password1"]')
        pw1.send_keys("fakestrongpassword091")
        pw2 = driver.find_element_by_xpath('//input[@name="password2"]')
        pw2.send_keys('fakestrongpassword091')
        pw2.send_keys(Keys.RETURN)

        driver.find_element_by_xpath("//a[text()='Register']").click()
        username = driver.find_element_by_xpath('//input[@name="username"]')
        username.send_keys(RANDOM_NAME)

        email = driver.find_element_by_xpath('//input[@name="email"]').click()
        driver.find_element_by_xpath('//input[@name="email"]').send_keys(Email)
        pw1 = driver.find_element_by_xpath('//input[@name="password1"]')
        pw1.send_keys("fakestrongpassword091!")
        pw2 = driver.find_element_by_xpath('//input[@name="password2"]')
        pw2.send_keys('fakestrongpassword091!')
        pw2.send_keys(Keys.RETURN)

        driver.find_element_by_xpath("//a[text()='Register']").click()
        username = driver.find_element_by_xpath('//input[@name="username"]')
        username.send_keys(RANDOM_NAME)

        email = driver.find_element_by_xpath('//input[@name="email"]').click()
        driver.find_element_by_xpath('//input[@name="email"]').send_keys(Email)
        pw1 = driver.find_element_by_xpath('//input[@name="password1"]')
        pw1.send_keys("100091")
        pw2 = driver.find_element_by_xpath('//input[@name="password2"]')
        pw2.send_keys('100091')
        pw2.send_keys(Keys.RETURN)

        driver.find_element_by_xpath('//a[text()="Login"]').click()
        driver.find_element_by_xpath('//input[@name="username"]').send_keys("WRONG NAME")
        driver.find_element_by_xpath('//input[@name = "password"]').send_keys(LEGAL_PASSWORD)
        driver.find_element_by_xpath('//button[text()="Login"]').click()
        eyes.check_window("error")
        assert("Please enter a correct username and password. Note that both fields may be case-sensitive." in driver.page_source)

        driver.find_element_by_xpath('//a[text()="Login"]').click()
        driver.find_element_by_xpath('//input[@name="username"]').send_keys(ran_name)
        driver.find_element_by_xpath('//input[@name = "password"]').send_keys("LEGAL_PASSWORD")
        driver.find_element_by_xpath('//button[text()="Login"]').click()
        assert("Please enter a correct username and password. Note that both fields may be case-sensitive." in driver.page_source)

        driver.find_element_by_xpath('//a[text()="Login"]').click()
        driver.find_element_by_xpath('//input[@name="username"]').send_keys(ran_name)
        driver.find_element_by_xpath('//input[@name = "password"]').send_keys(LEGAL_PASSWORD)
        driver.find_element_by_xpath('//button[text()="Login"]').click()

        eyes.check_window("Login-ed")

        # right = driver.find_element_by_xpath('//button[@class="fc-next-button fc-button fc-state-default fc-corner-right"]')
        # right.click()
        # eyes.check_window("today button lit up")

        # left=driver.find_element_by_xpath('        //button[@class="fc-prev-button fc-button fc-state-default fc-corner-left"]')
        # left.click()
        # eyes.check_window("today not lit")

        # driver.find_element_by_xpath('        //button[@class="fc-prev-button fc-button fc-state-default fc-corner-left"]').click()

        driver.set_window_size(300, 800)
        driver.set_window_position(0, 0)
        eyes.check_window("check collapse")

        driver.set_window_size(1536, 673)
        driver.set_window_position(0, 0)

        # show dropdown menu
        driver.find_element_by_xpath("//a[contains(text(),'Forms')]").click()
        eyes.check_window('Dropdown menu')

        driver.find_element_by_xpath("//a[contains(text(),'Schedule R')]").click()

        assert(driver.current_url == "http://localhost:8000/requestform/")

        driver.find_element_by_xpath("//a[contains(text(),'Forms')]").click()
        eyes.check_window('Dropdown menu')

        driver.find_element_by_xpath("//a[contains(text(),'Input M')]").click()

        assert(driver.current_url == "http://localhost:8000/requestform/input-module-info")

        driver.find_element_by_xpath("//a[contains(text(),'Forms')]").click()
        eyes.check_window('Dropdown menu')

        driver.find_element_by_xpath("//a[contains(text(),'In-vivo')]").click()

        assert(driver.current_url == "http://localhost:8000/requestform/add-event")

        driver.find_element_by_xpath("//a[contains(text(),'View R')]").click()

        assert(driver.current_url == "http://localhost:8000/requestform/view-requests")

        driver.find_element_by_xpath('//a[text()="Logout"]').click()
        eyes.check_window("logged out")

        eyes.close()

    finally:

        # Close the browser.
        driver.quit()

        # If the test was aborted before eyes.close was called, ends the test as aborted.
        eyes.abort_if_not_closed()
