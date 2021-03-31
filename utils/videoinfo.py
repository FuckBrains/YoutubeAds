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
import datetime

from utils.helpers import *
from utils.driverhelpers import *



def check_live(driver):
    container = driver.find_element_by_xpath('//span[@class="view-count style-scope ytd-video-view-count-renderer"]')
    if 'watching now' in container.text:
        return True
    else:
        return False

def check_removed(driver):
    try:
        container = driver.find_element_by_xpath('//div[@class="style-scope yt-player-error-message-renderer"]')
        inner = container.find_element_by_xpath('.//div[@id="reason"]')
        return True
    except:
        return False

def get_title(driver):
    return driver.find_element_by_xpath('//yt-formatted-string[@class="style-scope ytd-video-primary-info-renderer"]').text

def get_channel_info(driver):
    container = driver.find_element_by_xpath('//ytd-channel-name[@id="channel-name"]')
    channel = container.find_element_by_xpath('.//a[@class="yt-simple-endpoint style-scope yt-formatted-string"]')

    link = channel.get_attribute('href')
    link = removeprefix(link, 'https://www.youtube.com')

    if '/channel/' not in link:
        ID = link
    else:
        ID = removeprefix(link, '/channel/')

    return ID, channel.text

def get_views(driver):
    container = driver.find_element_by_xpath('//span[@class="view-count style-scope ytd-video-view-count-renderer"]')
    temp = removesuffix(container.text, ' views')
    temp = removesuffix(temp, ' watching now').replace(',', '')
    temp = removesuffix(temp, ' view')

    return int(temp)

def get_comment_count(driver):
    SCROLL_PAUSE_TIME = .5

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    found = False
    container = None

    count = 0
    while not found:
        try:
            # WebDriverWait(driver, 2).until(EC.presence_of_element_located(By.XPATH, '//yt-formatted-string[@class="count-text style-scope ytd-comments-header-renderer"]'))
            container = driver.find_element_by_xpath('//yt-formatted-string[@class="count-text style-scope ytd-comments-header-renderer"]')
            found = True
            # print('found comments')
        except:
            found = False

        if not found:
            # print('in scroll loop')
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, " + str(last_height/4) + ");")
            # print('scrolled')
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.documentElement.scrollHeight")

            # print(last_height)
            # print(new_height)    

            if (new_height == last_height) and count > 3:
                return -1
            last_height = new_height

        count += 1

    # container = driver.find_element_by_xpath('//yt-formatted-string[@class="count-text style-scope ytd-comments-header-renderer"]')
    return int("".join(list(filter(str.isdigit, container.text))))
    # return int(removesuffix(container.text, ' Comments').replace(',', ''))

def get_likes(driver):
    button_container = driver.find_element_by_xpath('//div[@id="top-level-buttons"]')
    containers = button_container.find_elements_by_xpath('.//yt-formatted-string[@class="style-scope ytd-toggle-button-renderer style-text"]')

    likes = -1
    dislikes = -1

    first = True
    for container in containers:
        # print(container.get_attribute('class'))
        aria_label = container.get_attribute('aria-label')
        if aria_label is None:
            aria_label = container.text


        aria_label = aria_label.replace(',', '')

        if aria_label == "No dislikes":
            dislikes = 0
        elif aria_label == "No likes":
            likes = 0
        elif 'dislike' in aria_label:
            try:
                dislikes = int("".join(list(filter(str.isdigit, aria_label))))
            except ValueError: 
                dislikes = -1
        else:
            try:
                likes = int("".join(list(filter(str.isdigit, aria_label))))
            except ValueError:
                likes = -1


    return likes, dislikes

def get_description(driver):
    try:
        driver.find_element_by_xpath('//yt-formatted-string[@class="less-button style-scope ytd-video-secondary-info-renderer"]')
        pass
    except:
        show_more = driver.find_element_by_xpath('//yt-formatted-string[@class="more-button style-scope ytd-video-secondary-info-renderer"]')
        show_more.click()

    container = driver.find_element_by_xpath('//div[@id="description"]')
    text_blocks = container.find_elements_by_xpath('.//span[@class="style-scope yt-formatted-string"]')
    # print(text_blocks)
    url_blocks = container.find_elements_by_xpath('.//a[@class="yt-simple-endpoint style-scope yt-formatted-string"]')

    # print(len(text_blocks), "text blocks")
    # print(len(url_blocks), "urls")

    text_index = 0
    url_index = 0

    descr_string = ""
    urls = []

    count = 0
    for text in text_blocks:
        # print("text", count, text.text)
        count += 1

    count = 0
    for url in url_blocks:
        # print("url", count, url.text)
        count += 1

    while text_index < len(text_blocks):
        # print('text', text_index, text_blocks[text_index].text)
        descr_string += text_blocks[text_index].text
        text_index += 1

        if url_index < len(url_blocks):
            # print('url', url_index, url_blocks[url_index].get_attribute("href"))
            # print('url text', url_index, url_blocks[url_index].text)
            url = get_descr_link(url_blocks[url_index].get_attribute("href"))
            descr_string += url
            urls.append(url)
            url_index += 1

            descr_string += ' '
            text_index += 1

    return descr_string, urls

def get_upload_date(driver):
    container = driver.find_element_by_xpath('//div[@id="date"]')
    date = container.find_element_by_xpath('.//yt-formatted-string[@class="style-scope ytd-video-primary-info-renderer"]').text
    date = removeprefix(date, "Started streaming on ")
    date = removeprefix(date, "Streamed live on ")
    date = removeprefix(date, "Premiered ")
    date_time_object = datetime.datetime.strptime(date, '%b %d, %Y')
    
    return date, int(date_time_object.timestamp())