from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException



import time
import sys
import re


def check_for_premium_ad(driver):
    try:
        skip_button = driver.find_element_by_xpath('//yt-formatted-string[text()="Skip trial"]')
        skip_button.click()
    except:
        pass


def check_preroll_info(driver):
    preroll_info = None

    try:
        preroll_info = WebDriverWait(driver, 2).until(EC.element_to_be_clickable(
            (By.XPATH, "//span[@class='ytp-ad-button-icon']")))
    except TimeoutException:
        pass

    return preroll_info

def check_for_premium_ad(driver):
    try:
        skip_button = driver.find_element_by_xpath('//yt-formatted-string[text()="Skip trial"]')
        skip_button.click()
    except:
        pass

# def check_number_of_ads(driver):
#     try:
#         ad_badge = driver.find_element_by_xpath('//[text()="Ad 1 of"]')
#         print("found multiple ads")
#         print(ad_badge.getText())
#     except:
#         pass

def check_preroll_or_banner(driver):
    try:
        pass
    except:
        pass


def check_preroll_info(driver):
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
        buttons = driver.find_elements_by_xpath('//span[@class="ytp-ad-button-icon"]')
        for item in buttons:
            print(item)
        if len(buttons) > 1:
            banner_info = buttons[1]

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

    result = driver.find_element_by_xpath("//ul[@class='ytp-ad-info-dialog-ad-reasons']")
    # results = result.find_elements_by_xpath("//li")

    for item in result.find_elements_by_xpath("//li"):
        toReturn.append(item.text)
    

    driver.find_element_by_xpath("//button[@class='ytp-ad-info-dialog-confirm-button']").click()

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

def play_video(driver):
    try:
        play_button = driver.find_element_by_xpath('//button[@class="ytp-large-play-button ytp-button"]')
        play_button.click()

    except:
        print('playing video failed')
        return 0

    return 1

def get_banner_advertiser(driver):
    try:
        ad_button = driver.find_element_by_xpath('//div[@class="ytp-ad-overlay-title"]')
        ad_button.click()
    except:
        try:
            ad_button = driver.find_element_by_xpath('//div[@class="ytp-ad-overlay-image"]')

            ad_button.click()
        except:
            return

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



def scroll_to_find_video(driver, video_index):
    videos = driver.find_elements_by_xpath("//a[@id='video-title']")
    print('scrolling')
    try:
        WebDriverWaeit(driver, 2).until(EC.visibility_of(
            videos[video_index]))
        found = True
    except:
        found = False


    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    print(last_height)

    while not found:
        print('in scroll loop')
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, " + str(last_height) + ");")
        print('scrolled')
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        print(new_height)
        if new_height == last_height:
            break
        last_height = new_height

        videos = driver.find_elements_by_xpath("//a[@id='video-title']")

        try:
            WebDriverWait(driver, 2).until(EC.visibility_of(
                videos[video_index]))
            found = True
            print('found video')
        except:
            found = False        

def skip_to(driver, number):
    # player = driver.find_element_by_xpath("//div[@id='player']")
    # player.send_keys(number)
    ActionChains(driver).key_down(number).key_up(number).perform()






def main():
    url_matcher = "^https?:\/\/[^#?\/]+"
    video_id_matcher = "watch\?v=[-\w]+"


    driver = webdriver.Firefox()
    actions = ActionChains(driver)


    base_url = 'https://www.youtube.com/watch?v='

    video_list = ['FDEYHxtimKk', 'KJ5UazhKXC8']

    data = []

    for video_id in video_list:

        driver.get(base_url + video_id)

        check_for_premium_ad(driver)

        played = play_video(driver)

        # time.sleep(6)

        if not played:
            continue

        results = []
        ad_url = None
        preroll_info = None
        banner_info = None


        preroll_info = check_preroll_info(driver)

        if preroll_info is not None:
            preroll_results = get_ad_info(driver, preroll_info)
            ad_url = get_preroll_advertiser(driver)

        # else:
        #     skip_to(driver, "5")
        #     time.sleep(6)
        #     banner_info = check_preroll_info(driver)
        #     if banner_info is not None:
        #         time.sleep(1)
        #         banner_results = get_ad_info(driver, banner_info)
        #         ad_url = get_banner_advertiser(driver)

        if ad_url:
            ad_url_base = re.search(url_matcher,ad_url)[0]
        else:
            ad_url_base = None

        toStore = {
            'videoId' : video_id,
            'videoName' : None,
            'channelId' : None,
            'channelName' : None,
            'views' : None,
            'comments' : None,
            'likes' : None,
            'descr' : None,
            'preroll' : False,
            'prerollAdvertiser' : None,
            'prerollFullUrl' : None,
            'prerollTargetingInfo' : None,
            'banner' : False,
            'bannerAdvertiser' : None,
            'bannerFullUrl' : None,
            'bannerTargetingInfo' : None,
            'dateCollected' : int(time.time()),
            'dateUploaded' : None,
            'classification' : None,
            'offSiteUrls' : None,
            'testId' : None
        }

        if preroll_info:
            toStore['preroll'] = True
            toStore['prerollAdvertiser'] = ad_url_base
            toStore['prerollFullUrl'] = ad_url
            toStore['prerollTargetingInfo'] = preroll_results

        if banner_info:
            toStore['banner'] = True
            toStore['bannerAdvertiser'] = ad_url_base
            toStore['bannerFullUrl'] = ad_url
            toStore['bannerTargetingInfo'] = banner_results


        data.append(toStore)

    print(data)



        



main()