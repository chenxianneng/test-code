#coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import utils
import time
import os
import datetime
from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn.mydb
my_set = db.circ_set

def make_dir(name):
    #保存裁判文书文档
    directory = utils.get_working_dir() + '/' + name + '/'
    if os.path.isdir(directory):
        pass
    else:
        os.mkdir(directory)

    return directory

def run(driver, save_dir, url ,browser='chrome'):
    
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(10)

    while True:
        elem = driver.find_element_by_xpath('//table[@id="ess_ctr14430_ModuleContent"]')
        trs = elem.find_elements_by_xpath('.//a[@target="_blank"]')
        print(len(trs))
        for tr in trs:
            tr.click()
            #点击进入执行信息
            #webdriver.ActionChains(driver).move_to_element(elem).click(elem).perform()

            title = tr.get_attribute('title')
            print(title)

            #选择标签
            driver.switch_to_window(driver.window_handles[1])
            content = driver.page_source

            content_elem = driver.find_element_by_id('tab_content')
            temp = content_elem.get_attribute('innerHTML')

            my_set.insert({'name':title, 'content':content_elem.get_attribute('innerText'), 'page_source':temp})
            
            #text = content.encode("gbk","ignore").decode("gbk")
    
            # #str_content = content.decode('utf-8')
            # file_name = save_dir + title + '.html'
            # #f = open(file_name, "w", encoding='gb18030')
            # f = open(file_name, "w", encoding='utf-8')
            # #temp = content.encode('utf-8')
            # f.write(content)
            # f.close()

            #关闭标签
            driver.close()
            driver.switch_to_window(driver.window_handles[0])

            time.sleep(1)

        elem = driver.find_element_by_link_text("下一页")
        href = elem.get_attribute('href')
        if href is not None:
            elem.click()
        else:
            break

dir_part_one = make_dir('保监会处罚')
dir_part_two = make_dir('保监局处罚')

# driver = utils.ChromeBrowser()
# run(driver, dir_part_one, 'http://bxjg.circ.gov.cn/web/site0/tab5240/')
#run(driver, dir_part_two, 'http://bxjg.circ.gov.cn/web/site0/tab5241/')


result = my_set.find({'content':{'$regex':"杨帆"}})
print(result.count())
for item in result:
    print(item['name'])
    file_name = 'D:/IPA/external/search_result.html'
    with open(file_name, "w") as f:
        encoding = '<meta http-equiv="Content-Type" content="text/html; charset=gb2312">'
        f.write(encoding)
        f.write(item['page_source'].replace('黑体', '')) #.encode("gbk","ignore").decode("gbk"))
        break

import pdfkit
pdfkit.from_file('D:/IPA/external/search_result.html', 'search_result.pdf')