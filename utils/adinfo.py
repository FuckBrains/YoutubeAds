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

from utils.driverhelpers import *
from utils.helpers import *
from constants.constants import *

import time



def check_for_preroll(driver):
    preroll_info = None

    try:
        preroll_info = WebDriverWait(driver, 2).until(EC.element_to_be_clickable(
            (By.XPATH, "//span[@class='ytp-ad-button-icon']")))
    except TimeoutException:
        pass

    return preroll_info

def check_banner_info(driver):
    banner_info = None

    try:
        container = driver.find_element_by_xpath('//div[@class="ytp-ad-overlay-container"]')
        banner_info = container.find_element_by_xpath('.//span[@class="ytp-ad-button-icon"]')
        # for item in buttons:
        #     print(item)

    except NoSuchElementException:
        pass

    return banner_info


def get_ad_info(driver, button):
    toReturn = []
    # try:
    # driver.execute_script("arguments[0].click();", button)
    button.click()
    # except:
    #     toReturn.append("unavailable")
    #     return toReturn
    try:
        result = driver.find_element_by_xpath("//ul[@class='ytp-ad-info-dialog-ad-reasons']")
        # results = result.find_elements_by_xpath("//li")

        for item in result.find_elements_by_xpath("//li"):
            toReturn.append(item.text)


        driver.find_element_by_xpath("//button[@class='ytp-ad-info-dialog-confirm-button']").click()
    except Exception as E:
        print("Get_ad_info exception", e)
        pass

    return toReturn

def get_preroll_advertiser(driver):
    ad_button = driver.find_element_by_xpath('//button[@class="ytp-ad-button ytp-ad-visit-advertiser-button ytp-ad-button-link"]')
    try:
        driver.execute_script("arguments[0].click();", ad_button)
        # ad_button.click()
    except:
        time.sleep(1)
        ad_button = driver.find_element_by_xpath('//button[@class="ytp-ad-button ytp-ad-visit-advertiser-button ytp-ad-button-link"]')
        ad_button.click()

    current_tab = driver.current_window_handle

    tabs_open = driver.window_handles

    driver.switch_to.window(tabs_open[1])

    loaded = False

    while not loaded:
        status = driver.execute_script("return document.readyState")
        loaded = status != "uninitialized"
    url = driver.current_url

    driver.close()
    driver.switch_to.window(current_tab)

    return url

def get_banner_advertiser(driver):
    ad_button = driver.find_element_by_xpath('//div[@class="ytp-ad-image-overlay"]')
    ad_button = ad_button.find_element_by_xpath('.//img')
    try:
        driver.execute_script("arguments[0].click();", ad_button)
        # ad_button.click()
    except Exception as e:
        print("first exception in banner advertiser", e)
        try:
            time.sleep(1)
            ad_button = driver.find_element_by_xpath('//div[@class="ytp-ad-image-overlay"]')
            ad_button.click()
        except Exception as f:
            print("second exception in banner advertiser", f)
            return None


    current_tab = driver.current_window_handle

    tabs_open = driver.window_handles

    driver.switch_to.window(tabs_open[1])

    loaded = False

    while not loaded:
        status = driver.execute_script("return document.readyState")
        loaded = status != "uninitialized"
    url = driver.current_url

    driver.close()
    driver.switch_to.window(current_tab)

    return url

def check_for_ads(driver):
    results = []
    ad_url = None
    ad_base_url = None
    ad_type = None
    ad_info = None

    preroll_info = check_for_preroll(driver)

    if preroll_info is not None:
        results = get_ad_info(driver, preroll_info)
        ad_url = get_preroll_advertiser(driver)
        ad_type = 'preroll'

    else:
        skip_to(driver, "5")
        time.sleep(4)
        banner_info = check_banner_info(driver)
        if banner_info is not None:
            try:
                ad_type = "banner"
                time.sleep(1)
                results = get_ad_info(driver, banner_info)
                ad_url = get_banner_advertiser(driver)
            except Exception as e:
                print('error in banner advertiser', e)
                pass

    if ad_url:
        ad_base_url = re.search(url_matcher, ad_url)[0]

    results = "&&&&".join(results)

    return results, ad_url, ad_base_url, ad_type

