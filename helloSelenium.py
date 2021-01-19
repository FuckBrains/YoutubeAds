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

# def check_number_of_ads(driver):
#     try:
#         ad_badge = driver.find_element_by_xpath('//[text()="Ad 1 of"]')
#         print("found multiple ads")
#         print(ad_badge.getText())
#     except:
#         pass

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


def get_ad_info(button):
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
        WebDriverWait(driver, 2).until(EC.visibility_of(
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


url_matcher = "^https?:\/\/[^#?\/]+"
video_id_matcher = "watch\?v=[-\w]+"


driver = webdriver.Firefox()
actions = ActionChains(driver)

driver.install_addon('C:\\Users\\Cameron\\Documents\\YouTube\\extension.xpi',temporary=True)

# driver.get('https://www.youtube.com/channel/UC9k23HZ1xMiqxf4gFfmxr5w')
driver.get('https://www.youtube.com/c/BroSanchez/')

ads = {}

try:
    tabs = driver.find_elements_by_xpath("//div[@class='tab-content style-scope paper-tab']")
    for tab in tabs:
        print(tab.text)
        if tab.text == 'VIDEOS':
            print('Found video tab')
            tab.click()
            break

    videos = driver.find_elements_by_xpath("//a[@id='video-title']")

    print(len(videos))

except:
    print("Couldn't get to channel videos")


for i in range(len(videos)):
    if i > 20: 
        break
    results = []
    check_for_premium_ad(driver)

    try:
        # scroll_to_find_video(driver, i)
        videos = driver.find_elements_by_xpath("//a[@id='video-title']")
        # print(videos[i].href)
        videos[i].click()
    except StaleElementReferenceException:
        driver.refresh()
        videos = driver.find_elements_by_xpath("//a[@id='video-title']")
        print('After refresh found', len(videos), 'videos.')
        print('Clicking video number', i)
        videos[i].click()

    video_id = re.search(video_id_matcher, driver.current_url)[0]
    
    results = []
    ad_url = None
    preroll_info = None
    banner_info = None

    # WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
    # (By.XPATH, "//button[@aria-label='Play']"))).click()

    # Look for preroll ads

    # try:
    preroll_info = check_preroll_info(driver)

    if preroll_info is not None:
        results = get_ad_info(preroll_info)

        # print("info in preroll ad is")
        # for item in results:
        #     print(item)

        ad_url = get_preroll_advertiser(driver)

    else:
        skip_to(driver, "5")
        time.sleep(1)
        banner_info = check_banner_info(driver)
        if banner_info is not None:
            results = get_ad_info(banner_info)

            # print("info in banner ad is: ")
            # for item in results:
            #     print(item)

            ad_url = get_banner_advertiser(driver)

    if ad_url:
        ad_url_base = re.search(url_matcher,ad_url)[0]

    toStore = {
        'preroll' : False,
        'preroll_advertiser' : None,
        'preroll_full_url' : None,
        'preroll_targeting_info' : None,
        'banner' : False,
        'banner_advertiser' : None,
        'banner_full_url' : None,
        'banner_targeting_info' : None
    }

    if preroll_info:
        toStore['preroll'] = True
        toStore['preroll_advertiser'] = ad_url_base
        toStore['preroll_full_url'] = ad_url
        toStore['preroll_targeting_info'] = results
    if banner_info:
        toStore['banner'] = True
        toStore['banner_advertiser'] = ad_url_base
        toStore['banner_full_url'] = ad_url
        toStore['banner_targeting_info'] = results


    ads[video_id[8:]] = toStore

    driver.back()

    # playbutton = driver.find_element_by_class_name('ytp-large-play-button ytp-button')

    # print(playbutton)

    # content = driver.find_element_by_class_name('ytp-ad-button-icon')

    # print(content)

print(ads)

driver.quit()