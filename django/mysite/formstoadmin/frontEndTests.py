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
import threading
import time


class EventScheduler_FrontEndTest:

    def __init__(self, test_registration=False):
        self.eyes = Eyes()
        self.eyes.api_key = 'IlUcgRAO105BlmoORdtUxbK8CUKg3KRSa8q4f3iACoY1I110'
        self.driver = webdriver.Chrome(r"C:\Users\Tea\Desktop\chromedriver_win32 (1)\chromedriver.exe")

        self.eyes.open(driver=self.driver, app_name='Hello World!', test_name='eventScheduler')
        self.driver.get('http://localhost:8000/')

        self.driver.set_window_size(1536, 673)
        self.driver.set_window_position(0, 0)

        self.eyes.check_window('Login')

        if test_registration == True:
            self.RANDOM_NAME = "100000"
            self.LEGAL_PASSWORD = 'SomeStrongPW09!'
            self.WEAK_PASSWORD = 'someweakpassword'

            self.ran_num = random.randint(1001, 5000)
            self.ran_num_str = str(self.ran_num)
            self.ran_name = "100" + self.ran_num_str
            self.Email = self.ran_name + '@mymail.sutd.edu.sg'

    def test_redirection(self):
        self.driver.find_element_by_xpath("//a[text()='Home']").click()
        self.eyes.check_window('Redirected to login')

        # show dropdown menu
        self.driver.find_element_by_xpath("//a[contains(text(),'Forms')]").click()
        self.eyes.check_window('Dropdown menu')

        self.driver.find_element_by_xpath("//a[contains(text(),'Schedule R')]").click()
        self.eyes.check_window('Redirected to login')

        assert(self.driver.current_url == "http://localhost:8000/login/?next=/requestform/")

    # test registration
    def test_registration_pass(self):
        self.driver.find_element_by_xpath("//a[text()='Register']").click()
        self.eyes.check_window('Registration page')

        username = self.driver.find_element_by_xpath('//input[@name="username"]')
        username.send_keys(self.ran_name)

        email = self.driver.find_element_by_xpath('//input[@name="email"]').click()
        self.eyes.check_window('Focused textbox')
        self.driver.find_element_by_xpath('//input[@name="email"]').send_keys(self.Email)

        pw1 = self.driver.find_element_by_xpath('//input[@name="password1"]')
        pw1.send_keys(self.LEGAL_PASSWORD)
        pw2 = self.driver.find_element_by_xpath('//input[@name="password2"]')
        pw2.send_keys(self.LEGAL_PASSWORD)
        pw2.send_keys(Keys.RETURN)

        self.eyes.check_window("Submitted")

    # re-registering with the same username
    def test_registration_repeatUser(self):
        self.driver.find_element_by_xpath("//a[text()='Register']").click()

        username = self.driver.find_element_by_xpath('//input[@name="username"]')
        username.send_keys(self.ran_name)

        email = self.driver.find_element_by_xpath('//input[@name="email"]').click()
        self.driver.find_element_by_xpath('//input[@name="email"]').send_keys(self.Email)

        pw1 = self.driver.find_element_by_xpath('//input[@name="password1"]')
        pw1.send_keys(self.LEGAL_PASSWORD)
        pw2 = self.driver.find_element_by_xpath('//input[@name="password2"]')
        pw2.send_keys(self.LEGAL_PASSWORD)
        pw2.send_keys(Keys.RETURN)

        assert('A user with that username already exists.' in self.driver.page_source)
        self.eyes.check_window("same user error message")

    # weak passwords
    def test_registration_fail(self):
        self.driver.find_element_by_xpath("//a[text()='Register']").click()

        # test weakpasswords
        username = self.driver.find_element_by_xpath('//input[@name="username"]')
        username.send_keys(self.RANDOM_NAME)

        email = self.driver.find_element_by_xpath('//input[@name="email"]').click()
        self.driver.find_element_by_xpath('//input[@name="email"]').send_keys(self.Email)

        pw1 = self.driver.find_element_by_xpath('//input[@name="password1"]')
        pw1.send_keys(self.WEAK_PASSWORD)
        pw2 = self.driver.find_element_by_xpath('//input[@name="password2"]')
        pw2.send_keys(self.WEAK_PASSWORD)
        pw2.send_keys(Keys.RETURN)

        self.driver.find_element_by_xpath("//a[text()='Register']").click()
        username = self.driver.find_element_by_xpath('//input[@name="username"]')
        username.send_keys(self.RANDOM_NAME)

        email = self.driver.find_element_by_xpath('//input[@name="email"]').click()
        self.driver.find_element_by_xpath('//input[@name="email"]').send_keys(self.Email)
        pw1 = self.driver.find_element_by_xpath('//input[@name="password1"]')
        pw1.send_keys("fakestrongpassword091")
        pw2 = self.driver.find_element_by_xpath('//input[@name="password2"]')
        pw2.send_keys('fakestrongpassword091')
        pw2.send_keys(Keys.RETURN)

        self.driver.find_element_by_xpath("//a[text()='Register']").click()
        username = self.driver.find_element_by_xpath('//input[@name="username"]')
        username.send_keys(self.RANDOM_NAME)

        email = self.driver.find_element_by_xpath('//input[@name="email"]').click()
        self.driver.find_element_by_xpath('//input[@name="email"]').send_keys(self.Email)
        pw1 = self.driver.find_element_by_xpath('//input[@name="password1"]')
        pw1.send_keys("fakestrongpassword091!")
        pw2 = self.driver.find_element_by_xpath('//input[@name="password2"]')
        pw2.send_keys('fakestrongpassword091!')
        pw2.send_keys(Keys.RETURN)

        self.driver.find_element_by_xpath("//a[text()='Register']").click()
        username = self.driver.find_element_by_xpath('//input[@name="username"]')
        username.send_keys(self.RANDOM_NAME)

        email = self.driver.find_element_by_xpath('//input[@name="email"]').click()
        self.driver.find_element_by_xpath('//input[@name="email"]').send_keys(self.Email)
        pw1 = self.driver.find_element_by_xpath('//input[@name="password1"]')
        pw1.send_keys("100091")
        pw2 = self.driver.find_element_by_xpath('//input[@name="password2"]')
        pw2.send_keys('100091')
        pw2.send_keys(Keys.RETURN)

    def test_login_wrong_username(self):
        self.driver.find_element_by_xpath('//a[text()="Login"]').click()
        self.driver.find_element_by_xpath('//input[@name="username"]').send_keys("WRONG NAME")
        self.driver.find_element_by_xpath('//input[@name = "password"]').send_keys(self.LEGAL_PASSWORD)
        self.driver.find_element_by_xpath('//button[text()="Login"]').click()
        self.eyes.check_window("error")
        assert("Please enter a correct username and password. Note that both fields may be case-sensitive." in self.driver.page_source)

    def test_login_wrong_pw(self):
        self.driver.find_element_by_xpath('//a[text()="Login"]').click()
        self.driver.find_element_by_xpath('//input[@name="username"]').send_keys(self.ran_name)
        self.driver.find_element_by_xpath('//input[@name = "password"]').send_keys("self.LEGAL_PASSWORD")
        self.driver.find_element_by_xpath('//button[text()="Login"]').click()
        assert("Please enter a correct username and password. Note that both fields may be case-sensitive." in self.driver.page_source)

    def test_login_pass(self):
        self.driver.find_element_by_xpath('//a[text()="Login"]').click()
        self.driver.find_element_by_xpath('//input[@name="username"]').send_keys(self.ran_name)
        self.driver.find_element_by_xpath('//input[@name = "password"]').send_keys(self.LEGAL_PASSWORD)
        self.driver.find_element_by_xpath('//button[text()="Login"]').click()

        self.eyes.check_window("Login-ed")

    def test_collapse(self):
        self.driver.set_window_size(300, 800)
        self.driver.set_window_position(0, 0)
        self.eyes.check_window("check collapse")

        self.driver.set_window_size(1536, 673)
        self.driver.set_window_position(0, 0)

    def test_dropdown(self):
        # show dropdown menu
        self.driver.find_element_by_xpath("//a[contains(text(),'Forms')]").click()
        self.eyes.check_window('Dropdown menu')

    def test_links(self):
        self.driver.find_element_by_xpath("//a[contains(text(),'Schedule R')]").click()

        assert(self.driver.current_url == "http://localhost:8000/requestform/")

        self.driver.find_element_by_xpath("//a[contains(text(),'Forms')]").click()
        self.eyes.check_window('Dropdown menu')

        self.driver.find_element_by_xpath("//a[contains(text(),'Input M')]").click()

        assert(self.driver.current_url == "http://localhost:8000/input-module-info")

        self.driver.find_element_by_xpath("//a[contains(text(),'Forms')]").click()
        self.eyes.check_window('Dropdown menu')

        self.driver.find_element_by_xpath("//a[contains(text(),'In-vivo')]").click()

        assert(self.driver.current_url == "http://localhost:8000/add-event")

        self.driver.find_element_by_xpath("//a[contains(text(),'Forms')]").click()
        self.driver.find_element_by_xpath("//a[contains(text(),'View R')]").click()

        assert(self.driver.current_url == "http://localhost:8000/view-requests")

    def logout(self):
        self.driver.find_element_by_xpath('//a[text()="Logout"]').click()
        self.eyes.check_window("logged out")

    def end(self):
        self.eyes.close()
        self.driver.quit()
        # If the test was aborted before self.eyes.close was called, ends the test as aborted.
        self.eyes.abort_if_not_closed()


test = EventScheduler_FrontEndTest(test_registration=True)

test.test_registration_pass()
test.test_login_pass()
test.test_collapse()
test.test_dropdown()
test.test_links()
test.logout()

test.end()
