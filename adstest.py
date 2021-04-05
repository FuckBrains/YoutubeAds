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

from utils.helpers import *
from utils.driverhelpers import *
from utils.videoinfo import *
from utils.adinfo import *
from constants.constants import *

import copy
import csv



def main():
    # Gen test ID and default config
    testid, test_str = get_test_id()
    config = {
        'headless' : False,
        'browser' : 'chrome',
        'mute' : True,
        'numvideos' : 10000,
        'iofreq' : 10,
        'username' : "csismymajor4444",
        'password' : "N01pbl0ckpls!!"
    }

    # ARG PARSE GOES HERE

    # Driver setup 
    if config['browser'] == 'firefox':
        options = webdriver.FirefoxOptions()
        if config['headless']:
            options.add_argument("-headless")
        if config['mute']:
            options.add_argument("--mute-audio")

        profile = webdriver.FirefoxProfile()
        if config['mute']:
            profile.set_preference("media.volume_scale", "0.0");

        driver = webdriver.Firefox(firefox_profile = profile, options = options)

    elif config['browser'] == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        # options.add_argument("--no-sandbox")
        if config['headless']:
            options.add_argument("--headless")
        if config['mute']:
            options.add_argument("--mute-audio")
        # options.add_argument("user-data-dir=User Data")
        driver = webdriver.Chrome(options = options)
        

    actions = ActionChains(driver)
    print('driver launched successfuly')

    if config['browser'] == 'firefox':
        # Login to account
        youtube_login(driver, config['username'], config['password'])
        print('logged into account ' + config['username'])

    # Setup output file
    keys = sample_entry.keys()
    output_file = open('tests/' + test_str + '.csv', 'w', newline='', encoding = 'utf-8') 
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()

    # Generate list of videos
    video_list = get_video_list('conspiracy_videos.txt', config['numvideos'])
    print("got video list")

    data = []
    count = 0
    for videoid in video_list:
        print('checking video ' + videoid)

        # Get collection time
        collectiontime = int(time.time())        

        # Load video
        driver.get(base_url + videoid)

        # This function dismisses the premium ad popup, gets called a few times
        check_for_premium_ad(driver)

        # Try to play video 
        played = play_video(driver)

        check_for_premium_ad(driver)

        #check if video was removed
        removed = check_removed(driver)

        if removed:
            # Get empty entry and return
            entry = copy.copy(sample_entry)
            entry['videoid'] = videoid
            entry['datecollected'] = collectiontime
            entry['testid'] = testid
            entry['played'] = played

            data.append(entry)
            continue


        if ((config['browser'] == 'firefox') and (not played)):
            print('Video not played')
            continue

        # Check for ads, returns None for each variable if no ad found
        results, adurl, adbaseurl, adtype = check_for_ads(driver)

        check_for_premium_ad(driver)

        # Check if video is live, changes some DOM elements
        islive = check_live(driver)

        # Get video title
        title = get_title(driver).encode("utf-8", 'ignore').decode('utf-8','ignore')
    
        # Get channel info
        channelID, channelName = get_channel_info(driver)
        # Strip non utf chars
        channelID = channelID.encode("utf-8", 'ignore').decode('utf-8','ignore')
        channelName = channelName.encode("utf-8", 'ignore').decode('utf-8','ignore')
        
        # Get view count
        views = get_views(driver)
        
        # If it's live, the engagement data is weird so we ignore it
        if islive:
            likes, dislikes, comments = -1, -1, -1
        # Else get likes and number of comments
        else:
            likes, dislikes = get_likes(driver)

            comments = get_comment_count(driver)

        # Get video description info and list of links 
        descr, descrurls = get_description(driver)

        # Strip non utf chars
        descr = descr.encode("utf-8", 'ignore').decode('utf-8','ignore')
        for i in range(len(descrurls)):
            descrurls[i] = descrurls[i].encode("utf-8", 'ignore').decode('utf-8','ignore')
        # Turn list of links into string for storage
        descrurls = "&&&&".join(descrurls)

        # Get upload date
        dateuploaded, uploadts = get_upload_date(driver)

        # Store data
        data.append({
            'videoid' : videoid,
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
            'adtype' : adtype,
            'advertiser' : adbaseurl,
            'adfullurl' : adurl,
            'targetinginfo' : results,
            'datecollected' : collectiontime,
            'dateuploaded' : dateuploaded,
            'uploadts' : uploadts,
            'classification' : None,
            'testid' : testid,
            'removed' : False,
            'played' : played
        })

        count += 1
        if ((count % config['iofreq']) == 0):
            dict_writer.writerows(data)
            data = []



main()