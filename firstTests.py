from selenium import webdriver

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


import datetime
import time
import sys
import re
import pprint


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
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ytp-large-play-button ytp-button"]')))
        play_button = driver.find_element_by_xpath('//button[@class="ytp-large-play-button ytp-button"]')
        play_button.click()

    except Exception as e:
        print(e)
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
        WebDriverWait(driver, 2).until(EC.visibility_of(videos[video_index]))
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

def removeprefix(instr, prefix):
    if instr.startswith(prefix):
        return instr[len(prefix):]
    else:
        return instr[:]

def removesuffix(instr, suffix):

    if suffix and instr.endswith(suffix):
        return instr[:-len(suffix)]
    else:
        return instr[:]

def skip_to(driver, number):
    # player = driver.find_element_by_xpath("//div[@id='player']")
    # player.send_keys(number)
    ActionChains(driver).key_down(number).key_up(number).perform()


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
    container = driver.find_element_by_xpath('//span[@class="view-count style-scope yt-view-count-renderer"]')
    temp = removesuffix(container.text, ' views')
    temp = removesuffix(temp, ' watching now').replace(',', '')

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
            print('found comments')
        except:
            found = False

        if not found:
            print('in scroll loop')
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, " + str(last_height/4) + ");")
            print('scrolled')
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.documentElement.scrollHeight")

            print(last_height)
            print(new_height)    

            if (new_height == last_height) and count > 3:
                return -1
            last_height = new_height

        count += 1

        


    # container = driver.find_element_by_xpath('//yt-formatted-string[@class="count-text style-scope ytd-comments-header-renderer"]')
    return int(removesuffix(container.text, ' Comments').replace(',', ''))

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

        if 'dislike' in aria_label:
            dislikes = int("".join(list(filter(str.isdigit, aria_label))))

        else:
            likes = int("".join(list(filter(str.isdigit, aria_label))))


    return likes, dislikes

def get_descr_link(link_text):
    search = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

    temp = removeprefix(link_text, "https://www.youtube.com/")

    temp = temp.replace("%3A", ":")
    temp = temp.replace("%2F", "/")

    if re.search(search,temp) is None:
        re.search(search,temp)
        return link_text
    else:
        url = re.search(search,temp)[0]

        return url


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
    date = removeprefix(date, "Premiered ")
    date_time_object = datetime.datetime.strptime(date, '%b %d, %Y')
    
    return date, int(date_time_object.timestamp())

def check_live(driver):
    container = driver.find_element_by_xpath('//span[@class="view-count style-scope yt-view-count-renderer"]')
    if 'watching now' in container.text:
        return True
    else:
        return False




def main():
    url_matcher = "^https?:\/\/[^#?\/]+"
    video_id_matcher = "watch\?v=[-\w]+"

    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    options.add_argument("--mute-audio")

    profile = webdriver.FirefoxProfile()
    profile.set_preference("media.volume_scale", "0.0");

    driver = webdriver.Firefox(firefox_profile = profile, options = options)
    actions = ActionChains(driver)


    base_url = 'https://www.youtube.com/watch?v='

    video_list = ['KJ5UazhKXC8', 'FDEYHxtimKk', '0te6noMKffA', 'ownHh9QIsRk', 'tutZKLeGrCs', '0JW7_HRWahU', 'Pyzg3biuz1Q', 'P_6my53IlxY', 'O7cwFYAQvEU', 'JqhOPUVE9Os', '6lOgh8torPA', 'Ldc5aG_1Q7o', 'IZ_8b_Ydsv0', 'o27tIdYggY0', 'H6uBaP0KoWg']

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

        islive = check_live(driver)

        title = get_title(driver)

        channelID, channelName = get_channel_info(driver)

        views = get_views(driver)

        if islive:
            likes, dislikes, comments = -1, -1, -1

        else:
            likes, dislikes = get_likes(driver)

            comments = get_comment_count(driver)

        descr, descrurls = get_description(driver)

        dateuploaded, uploadts = get_upload_date(driver)

        

        # if not live:
        #     likes, dislikes = get_likes(driver)

        #     comments = get_comment_count(driver)
        # else:
        #     likes, dislikes, comments = 0, 0, 0

        toStore = {
            'videoid' : video_id,
            'videoname' : title,
            'channelid' : channelID,
            'channelname' : channelName,
            'islive' : islive,
            'views' : views,
            'comments' : comments,
            'likes' : likes,
            'dislikes' : dislikes,
            'descr' : descr,
            'descrurls' : descrurls,
            'preroll' : False,
            'prerolladvertiser' : None,
            'prerollfullurl' : None,
            'prerolltargetinginfo' : None,
            'banner' : False,
            'banneradvertiser' : None,
            'bannerfullurl' : None,
            'bannertargetinginfo' : None,
            'datecollected' : int(time.time()),
            'dateuploaded' : dateuploaded,
            'uploadts' : uploadts,
            'classification' : None,
            'testid' : None
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

    pp = pprint.PrettyPrinter(indent = 4)
    pp.pprint(data)

    driver.quit()




        



main()