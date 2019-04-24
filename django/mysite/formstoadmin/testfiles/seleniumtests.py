from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

from django.test import TestCase
import threading
import time
import random
import logging
import datetime

LEGAL_PASSWORD = 'testing321'

''' Helper Functions '''


def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def yes_or_no():
    ran_num = random.randint(1, 2)
    if ran_num == 1:
        return True
    else:
        return False


def get_ran_num(min=0, max=100):
    return random.randint(min, max)


def generate_user():
    ran_num = random.randint(1001, 5000)
    ran_num_str = str(ran_num)
    ran_name = "100" + ran_num_str
    email = ran_name + '@mymail.sutd.edu.sg'
    return ran_name, email


chrome_options = Options()
# chrome_options.add_argument("headless")
chrome_options.add_argument("allow-insecure-localhost")
driver = webdriver.Chrome(r"C:\Users\Tea\Desktop\chromedriver_win32 (1)\chromedriver.exe", options=chrome_options)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
logger = setup_logger('info_level_logger', 'formsINFO.log')


def setup(login=False, user_level=3):
    self.driver.get('http://localhost:8000/')
    if login == True:
        if user_level == 3:
            login("huanan", "testing321")


def register():
    ran_name, email = generate_user()
    driver.find_element_by_xpath("//a[text()='Register']").click()
    username = driver.find_element_by_xpath('//input[@name="username"]')
    username.send_keys(ran_name)

    driver.find_element_by_xpath('//input[@name="email"]').send_keys(email)

    pw1 = driver.find_element_by_xpath('//input[@name="password1"]')
    pw1.send_keys(LEGAL_PASSWORD)
    pw2 = driver.find_element_by_xpath('//input[@name="password2"]')
    pw2.send_keys(LEGAL_PASSWORD)
    pw2.send_keys(Keys.RETURN)

    success_msg = driver.find_element_by_class_name('.alert.alert-success')
    assert f"Account created for {username}" in success_msg


def login(username, password=LEGAL_PASSWORD):
    driver.find_element_by_xpath('//a[text()="Login"]').click()
    driver.find_element_by_xpath('//input[@name="username"]').send_keys(username)
    driver.find_element_by_xpath('//input[@name = "password"]').send_keys(password)
    driver.find_element_by_xpath('//button[text()="Login"]').click()


def add_event():
    driver.find_element_by_id("id_persons_in_charge").click().send_keys()
    driver.find_element_by_id("id_event_name").click().send_keys()
    checkboxes = driver.find_elements_by_class_name('form-check-input')
    for i in checkboxes:
        if yes_or_no() == True:
            i.click()
    ran_num = get_ran_num()
    driver.find_elements_by_id('id_duration').send_keys(ran_num)
    driver.find_elements_by_id('id_num_people').send_keys(ran_num)
    driver.find_elements_by_id('id_date').send_keys("28/4/2019")
    submit = driver.find_elements_by_id('add-event-submit').click()


setup(login=True)
