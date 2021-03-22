from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


import datetime
import time
import sys
import re
import pprint
import csv
import random


def main():
    options = webdriver.FirefoxOptions()
    # options.add_argument("-headless")
    options.add_argument("--mute-audio")

    profile = webdriver.FirefoxProfile()
    profile.set_preference("media.volume_scale", "0.0");

    driver = webdriver.Firefox(firefox_profile = profile, options = options)
    actions = ActionChains(driver)

    print('driver launched successfuly')

    signinurl = "https://accounts.google.com/signin/v2/identifier?service=youtube"

    username = "csismymajor4444"
    password = "N01pbl0ckpls!!"

    driver.get(signinurl)
    uEntry = driver.find_element_by_id("identifierId")
    uEntry.clear()
    uEntry.send_keys(username)

    nextButton = driver.find_element_by_xpath('//span[text()="Next"]')
    nextButton = nextButton.find_element_by_xpath('./..')
    nextButton.click()

    # WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]')))
    WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, 'password')))
    pEntry = driver.find_element_by_id("password")
    pEntry = pEntry.find_element_by_xpath('.//input[@type="password"]')
    pEntry.clear()
    pEntry.send_keys(password)
    time.sleep(1)
    pEntry.send_keys(Keys.RETURN)

    # passwordNext = driver.find_element_by_id("passwordNext")
    # # passwordNext.click()
    # nextButton = passwordNext.find_element_by_xpath('.//span[text()="Next"]')
    # nextButton = nextButton.find_element_by_xpath('./..')
    # nextButton.click()

main()