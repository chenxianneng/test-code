from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from you_get import common as you_get

directory = r'D:/1'

driver = webdriver.Chrome()
driver.get('https://www.youtube.com/channel/UC-9-kyTW8ZkZNDHQJ6FgpwQ')
driver.maximize_window()
driver.implicitly_wait(10)

elems = driver.find_elements_by_xpath(".//a[@class='yt-simple-endpoint style-scope ytd-grid-video-renderer']")
print(len(elems))
for elem in elems:
    time.sleep(3)
    href = elem.get_attribute('href')
    url = 'https://www.youtube.com' + href
    print(url)
    
    try:
        sys.argv = ['you-get', '-o', directory, url]
        you_get.main()
    except Exception as e:
        pass
