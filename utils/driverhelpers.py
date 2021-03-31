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

import time

from constants.constants import *



def play_video(driver):
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ytp-large-play-button ytp-button"]')))
        play_button = driver.find_element_by_xpath('//button[@class="ytp-large-play-button ytp-button"]')
        play_button.click()

    except Exception as e:
        # print(e)
        # print('playing video failed')
        return False

    return True

def skip_to(driver, number):
    # player = driver.find_element_by_xpath("//div[@id='player']")
    # player.send_keys(number)
    ActionChains(driver).key_down(number).key_up(number).perform()

def check_for_premium_ad(driver):
    try:
        # print('check 1')
        skip_button = driver.find_element_by_xpath('//ytd-button-renderer[@id="dismiss-button"]')
        skip_button = skip_button.find_element_by_xpath('//paper_button[@id="button"]')
        skip_button.click()
        # print('clicked')
    except Exception as e:
        # print(e)
        pass

def youtube_login(driver, username, password):
    signinurl = "https://accounts.google.com/signin/v2/identifier?service=youtube"
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
    time.sleep(2)
