from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

import traceback
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


def get_ran_num(start=0, end=200):
    return random.randint(start, end)


def generate_user():
    ran_num = random.randint(1001, 5000)
    ran_num_str = str(ran_num)
    ran_name = "100" + ran_num_str
    email = ran_name + '@mymail.sutd.edu.sg'
    return ran_name, email


def bid(p):
    return driver.find_element_by_id(p)


def bxpath(p):
    return driver.find_element_by_xpath(p)


def bclass(p):
    return driver.find_element_by_class_name(p)


chrome_options = Options()
# chrome_options.add_argument("headless")
chrome_options.add_argument("allow-insecure-localhost")
driver = webdriver.Chrome(r"C:\Users\Tea\Desktop\chromedriver_win32 (1)\chromedriver.exe", options=chrome_options)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
logger = setup_logger('info_level_logger', 'formsINFO.log')


def setup(_login=False, user_level=3):
    driver.get('http://localhost:8000/')
    if _login == True:
        if user_level == 3:
            login(username="huanan", password="testing321")


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


def login(username="huanan", password=LEGAL_PASSWORD):
    driver.find_element_by_xpath('//a[text()="Login"]').click()
    driver.find_element_by_xpath('//input[@name="username"]').send_keys(username)
    driver.find_element_by_xpath('//input[@name = "password"]').send_keys(password)
    driver.find_element_by_xpath('//button[text()="Login"]').click()


def add_event():
    bid("navbarDropdown").click()
    bxpath('//a[text()="In-vivo Event"]').click()
    logger.info(f"add-event url:{driver.current_url}")

    driver.find_element_by_id("id_persons_in_charge").send_keys("Person A, Person B")
    ran_num = get_ran_num()
    driver.find_element_by_id("id_event_name").send_keys(f"Event {ran_num}")
    checkboxes = driver.find_elements_by_class_name('form-check-input')
    for i in checkboxes:
        if yes_or_no() == True:
            i.click()
    ran_num = get_ran_num()
    driver.find_element_by_id('id_duration').send_keys(ran_num)
    driver.find_element_by_id('id_num_people').send_keys(ran_num)
    driver.find_element_by_id('id_date').send_keys("28/4/2019")
    submit = driver.find_element_by_id('add-event-submit').click()

    bxpath('button[@class="close"]').click()
    bxpath('//a[text()="View Suggestions"]').click()
    bxpath('//a[text()="Accept"]').click()
    obj = driver.switch_to.alert()
    msg = obj.text
    logger.info(f'alert dialog message: {msg}')
    obj.dismiss()

    bxpath('//a[text()="Accept"]').click()
    obj = driver.switch_to.alert()
    obj.accept()


def schedule_request():
    bid("navbarDropdown").click()
    bxpath('//a[text()="Schedule Request"]').click()
    logger.info(f"schedule-request url:{driver.current_url}")

    select = Select(bid('id_course_name'))
    logger.info(f"\nCourses in schedule request: {select.options}")
    ran_num = get_ran_num(end=len(select.options))
    for index in range(ran_num):
        select = Select(bid('id_course_name'))
        select.select_by_index(index)

    ran_num = get_ran_num()
    bid('id_duration').send_keys(ran_num)
    bid('id_class_related').send_keys("5CISTD01, 5CISTD02")
    checkboxes = driver.find_elements_by_class_name('form-check-input')
    for i in checkboxes:
        if yes_or_no() == True:
            i.click()
    bid('id_reasons').send_keys("I have my reasons")
    if yes_or_no():
        bid('id_remarks').send_keys("I'll buy you coffee!")
    bxpath('//button[text()="Submit"]').click()
    success = bclass('alert-success')
    assert success.text == "Request submitted"


def input_mod_info():
    bid("navbarDropdown").click()
    bxpath('//a[text()="Input Module Information"]').click()
    logger.info(f"\ninput-module-info url:{driver.current_url}")

    bid('id_subject_code').send_keys("02.131")
    bid('id_subject').send_keys('Documentary')
    select = Select(bid('id_pillar'))
    logger.info(f"Pillars: {select.options}")
    ran_num = get_ran_num(end=len(select.options))
    for index in range(ran_num):
        select = Select(bid('id_pillar'))
        select.select_by_index(index)

    ran_num = get_ran_num(start=1, end=8)
    bid('id_term').send_keys(ran_num)
    result = str(yes_or_no())
    bid('id_core').send_keys(result)

    bid('id_subject_lead').send_keys("Sandeep Ray")
    ran_num = get_ran_num()
    bid('id_cohort_size').send_keys(ran_num)
    ran_num = get_ran_num()
    bid('id_enrolment_size').send_keys(ran_num)
    ran_num = get_ran_num(start=1, end=10)
    bid('id_cohorts').send_keys(ran_num)
    ran_num = get_ran_num(end=3)
    bid('id_cohorts_per_week').send_keys(ran_num)
    ran_num = get_ran_num(end=3)
    bid('id_lectures_per_week').send_keys(ran_num)
    ran_num = get_ran_num(end=2)
    bid('id_labs_per_week').send_keys(ran_num)
    bxpath('//button[text()="Submit"]').click()
    assert bclass('alert-success')


def upload_modules_via_csv():
    bid("navbarDropdown").click()
    bxpath('//a[text()="Input Module Information"]').click()
    bxpath('//a[contains(text(),"CSV")]').click()
    logger.info(f"\ninput-module-info-by-csv url:{driver.current_url}")
    choose_btn = bxpath('//input[@type="file"]')
    choose_btn.send_keys(r'C:\Users\Tea\Desktop\50.003 Event Scheduler\sutd-scheduler-db\django\mysite\formstoadmin\testfiles\SampleModuleData_Correct.csv')
    bxpath('//button[text()="Upload"]').click()
    assert bclass('alert-success')
    assert "Uploaded file" in driver.page_source

    choose_btn.send_keys(r'C:\Users\Tea\Desktop\50.003 Event Scheduler\sutd-scheduler-db\django\mysite\formstoadmin\testfiles\SampleModuleData_EmptyCells.csv')
    bxpath('//button[text()="Upload"]').click()
    assert bclass('alert-success')

    choose_btn.send_keys(r'C:\Users\Tea\Desktop\50.003 Event Scheduler\sutd-scheduler-db\django\mysite\formstoadmin\testfiles\SampleModuleData_WrongNumColumns.csv')
    bxpath('//button[text()="Upload"]').click()
    assert bclass('alert-error')


def input_class_info():
    bid("navbarDropdown").click()
    bxpath('//a[text()="Input Class Information"]').click()

    select = Select(bid('id_module'))
    logger.info(f"Pillars: {select.options}")
    ran_num = get_ran_num(end=len(select.options))
    for index in range(ran_num):
        select = Select(bid('id_module'))
        select.select_by_index(index)

    bxpath('//button[@type="submit"]').click()
    bxpath('//a[contains(text(),"Back")]').click()
    assert driver.current_url == "http://localhost:8000/input-class-info-start/"
    driver.back()

    # EYES
    bid('id_location').send_keys("CC13")

    # To assert fill out this field pop up present
    bxpath('//button[@type="submit"]').click()
    # EYES

    result = str(yes_or_no())
    bid('id_makeup').send_keys(result)
    ran_num = get_ran_num()
    bid('id_description').send_keys(f"Just as an identifier:{ran_num}")
    bxpath('//button[@type="submit"]').click()
    assert bclass('alert-success')
    # EYES
    prev = bxpath('//a[contains(text(),"Previous")]')
    Next = bxpath('//a[contains(text(),"Next")]')

    ''' Checking disabled button is disabled '''
    current_url = driver.current_url
    prev.click()
    assert driver.current_url == current_url


def view_requests():
    bid("navbarDropdown").click()
    bxpath('//a[text()="View Requests"]').click()


def logout():
    driver.find_element_by_xpath('//a[text()="Logout"]').click()


def end():
    driver.quit()


try:
    setup(_login=True, mobile=False)
    # add_event()
    # schedule_request()
    # input_mod_info()
    # upload_modules_via_csv()
    input_class_info()
except Exception:
    traceback.print_exc()
# finally:
#     logout()
#     end()
