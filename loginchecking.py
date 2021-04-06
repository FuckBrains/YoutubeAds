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



options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless")
options.add_argument("--mute-audio")
options.add_argument("user-data-dir=C:\\Users\\Cameron\\Documents\\YoutubeAds\\UserData")
# options.add_argument("user-data-dir=C:\\Users\\Cameron\\AppData\\Local\\Google\\Chrome\\User Data")

driver = webdriver.Chrome(options = options)
driver.get("https://www.gmail.com")

print(driver.title)
assert(driver.title == "Inbox - csismymajor4444@gmail.com - Gmail")


driver.quit()


