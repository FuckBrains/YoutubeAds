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
        # print('check 1')
        skip_button = driver.find_element_by_xpath('//ytd-button-renderer[@id="dismiss-button"]')
        skip_button = skip_button.find_element_by_xpath('//paper_button[@id="button"]')
        skip_button.click()
        # print('clicked')
    except Exception as e:
        # print(e)
        pass

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
        # for item in buttons:
        #     print(item)
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
        # print(e)
        # print('playing video failed')
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
    # print('scrolling')
    try:
        WebDriverWait(driver, 2).until(EC.visibility_of(videos[video_index]))
        found = True
    except:
        found = False


    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    # print(last_height)

    while not found:
        # print('in scroll loop')
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, " + str(last_height) + ");")
        # print('scrolled')
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        # print(new_height)
        if new_height == last_height:
            break
        last_height = new_height

        videos = driver.find_elements_by_xpath("//a[@id='video-title']")

        try:
            WebDriverWait(driver, 2).until(EC.visibility_of(
                videos[video_index]))
            found = True
            # print('found video')
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
    date = removeprefix(date, "Streamed live on ")
    date = removeprefix(date, "Premiered ")
    date_time_object = datetime.datetime.strptime(date, '%b %d, %Y')
    
    return date, int(date_time_object.timestamp())

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


def get_video_list(filename, num_videos):
    infile = open(filename, 'r')
    video_list = []
    for line in infile:
        video_list.append(line.strip())

    infile.close()

    random.shuffle(video_list)

    return video_list[:num_videos]

def update_test_id():
    test_file = open('test_id.txt', 'r')
    for line in test_file:
        test_num = int(line)
    # test_num = int(test_file.readline())

    test_file.close()

    test_file = open('test_id.txt', 'w')
    test_file.write(str(test_num + 1))
    test_file.close()

    return test_num + 1


def get_test_id():
    d = datetime.datetime.now()
    test_str = '{date:%Y_%m_%d_%H_%M_%S}'.format(date = d)
    test_id = int('{date:%Y%m%d%H%M%S}'.format(date = d))

    return test_id, test_str


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



def main():
    test_id, test_str = get_test_id()

    url_matcher = "^https?:\/\/[^#?\/]+"
    video_id_matcher = "watch\?v=[-\w]+"

    options = webdriver.FirefoxOptions()
    # options.add_argument("-headless")
    options.add_argument("--mute-audio")

    profile = webdriver.FirefoxProfile()
    profile.set_preference("media.volume_scale", "0.0");

    driver = webdriver.Firefox(firefox_profile = profile, options = options)
    actions = ActionChains(driver)

    print('driver launched successfuly')

    username = "csismymajor4444"
    password = "N01pbl0ckpls!!"
    youtube_login(driver, username, password)
    print('logged into account ' + username)

    base_url = 'https://www.youtube.com/watch?v='

    sample_entry = {
            'videoid' : None,
            'videoname' : None,
            'channelid' : None,
            'channelname' : None,
            'islive' : None,
            'views' : None,
            'comments' : None,
            'likes' : None,
            'dislikes' : None,
            'descr' : None,
            'descrurls' : None,
            'adtype' : None,
            'advertiser' : None,
            'adfullurl' : None,
            'targetinginfo' : None,
            'datecollected' : None,
            'dateuploaded' : None,
            'uploadts' : None,
            'classification' : None,
            'testid' : None,
            'removed' : None
    }

    keys = sample_entry.keys()
    output_file = open(test_str + '.csv', 'w', newline='', encoding = 'utf-8') 
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()


    # video_list = ['1KKUD7c8wo8', 'KJ5UazhKXC8', 'FDEYHxtimKk', '0te6noMKffA', 'ownHh9QIsRk', 'tutZKLeGrCs', '0JW7_HRWahU', 'Pyzg3biuz1Q', 'P_6my53IlxY', 'O7cwFYAQvEU', 'JqhOPUVE9Os', '6lOgh8torPA', 'Ldc5aG_1Q7o', 'IZ_8b_Ydsv0', 'o27tIdYggY0', 'H6uBaP0KoWg']
    
    video_list = get_video_list('conspiracy_videos.txt', 100)
    print("got video list")

    data = []
    count = 0

    for video_id in video_list:
        print('checking video ' + video_id)

        collection_time = int(time.time())        

        driver.get(base_url + video_id)

        check_for_premium_ad(driver)

        played = play_video(driver)

        check_for_premium_ad(driver)

        removed = check_removed(driver)

        if removed:
            data.append({
            'videoid' : video_id,
            'videoname' : None,
            'channelid' : None,
            'channelname' : None,
            'islive' : None,
            'views' : None,
            'comments' : None,
            'likes' : None,
            'dislikes' : None,
            'descr' : None,
            'descrurls' : None,
            'adtype' : None,
            'advertiser' : None,
            'adfullurl' : None,
            'targetinginfo' : None,
            'datecollected' : collection_time,
            'dateuploaded' : None,
            'uploadts' : None,
            'classification' : None,
            'testid' : test_id,
            'removed' : True
            })
            continue


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

        check_for_premium_ad(driver)

        islive = check_live(driver)

        title = get_title(driver).encode("utf-8", 'ignore').decode('utf-8','ignore')
    
        channelID, channelName = get_channel_info(driver)
        channelID = channelID.encode("utf-8", 'ignore').decode('utf-8','ignore')
        channelName = channelName.encode("utf-8", 'ignore').decode('utf-8','ignore')
        
        
        views = get_views(driver)
        

        if islive:
            likes, dislikes, comments = -1, -1, -1

        else:
            likes, dislikes = get_likes(driver)

            comments = get_comment_count(driver)

        descr, descrurls = get_description(driver)

        descr = descr.encode("utf-8", 'ignore').decode('utf-8','ignore')
        for i in range(len(descrurls)):
            descrurls[i] = descrurls[i].encode("utf-8", 'ignore').decode('utf-8','ignore')
        descrurls = "&&&&".join(descrurls)

        dateuploaded, uploadts = get_upload_date(driver)

        prerollStore = {
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
            'adtype' : "preroll",
            'advertiser' : None,
            'adfullurl' : None,
            'targetinginfo' : None,
            'datecollected' : collection_time,
            'dateuploaded' : dateuploaded,
            'uploadts' : uploadts,
            'classification' : None,
            'testid' : test_id,
            'removed' : False
        }

        bannerStore = {
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
            'adtype' : "banner",
            'advertiser' : None,
            'adfullurl' : None,
            'targetinginfo' : None,
            'datecollected' : collection_time,
            'dateuploaded' : dateuploaded,
            'uploadts' : uploadts,
            'classification' : None,
            'testid' : test_id,
            'removed' : False
        }        

        # if not live:
        #     likes, dislikes = get_likes(driver)

        #     comments = get_comment_count(driver)
        # else:
        #     likes, dislikes, comments = 0, 0, 0

        if preroll_info:
            preroll_results = "&&&&".join(preroll_results)

        if preroll_info:
            prerollStore['advertiser'] = ad_url_base
            prerollStore['adfullurl'] = ad_url
            prerollStore['targetinginfo'] = preroll_results
            data.append(prerollStore)

        if banner_info:
            bannerStore['advertiser'] = ad_url_base
            bannerStore['adfullurl'] = ad_url
            bannerStore['targetinginfo'] = preroll_results
            data.append(bannerStore)

        if not (preroll_info or  banner_info):
            prerollStore['adtype'] = None
            data.append(prerollStore)

        count += 1
        if ((count % 10) == 0):
            dict_writer.writerows(data)
            data = []


    # pp = pprint.PrettyPrinter(indent = 4)
    # pp.pprint(data)

    print('shutting down')

    dict_writer.writerows(data)

    driver.quit()
    output_file.close()


        


        



main()
