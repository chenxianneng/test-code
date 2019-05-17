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
my_set = db.cbrc_set

def make_dir(name):
    #保存裁判文书文档
    directory = utils.get_working_dir() + '/' + name + '/'
    if os.path.isdir(directory):
        pass
    else:
        os.mkdir(directory)

    return directory

def stop_catche(limit_date, record_date):
    temp1 = limit_date.split('-')
    temp2 = record_date.split('-')
    a, b = [], []
    for i in temp1:
        a.append(int(i))

    d1 = datetime.datetime(a[0], a[1], a[2]) 
        
    for i in temp2:
        b.append(int(i))

    d2 = datetime.datetime(b[0], b[1], b[2])

    return record_date < limit_date
        
def run(driver, save_dir, url, limit_date=None , browser='chrome'):    
    driver.get(url)
    #driver.maximize_window()
    driver.implicitly_wait(10)
    
    while True:
        elem = driver.find_element_by_xpath('//*[@id="testUI"]')
        #elem.find_elements_by_xpath('')
        #trs = elem.find_elements_by_xpath(".//a")
        a_tags = elem.find_elements_by_xpath(".//a[@class='STYLE8']")
        print(len(a_tags))
        for a_tag in a_tags:
            parent = a_tag.find_element_by_xpath('..')
            record_date = parent.find_element_by_xpath("following::td")
            temp = record_date.get_attribute('innerText').split('-')
            print(temp)
            
            date = datetime.datetime(int(temp[0]), int(temp[1]), int(temp[2]))

            if limit_date is not None and stop_catche(limit_date, record_date):
                driver.quit()
                return
            
            a_tag.click()
            title = a_tag.get_attribute('title')
            print(title)

            #选择标签
            driver.switch_to_window(driver.window_handles[1])

            content = driver.page_source
            #page_source = content.encode("gbk","ignore").decode("gbk")
            
            content_elem = driver.find_element_by_class_name('n_cent')
            temp = content_elem.get_attribute('innerHTML') #.encode("gbk","ignore").decode("gbk")

            # file_name = save_dir + title + '.html'
            # f = open(file_name, "w")
            # f.write(text)
            # f.close()

            # file_name = "test.txt"
            # f = open(file_name, "w")
            # f.write(content_elem.get_attribute('innerText').encode("gbk","ignore").decode("gbk"))
            # f.close()
            # return 

            my_set.insert({'name': title, \
                'content': content_elem.get_attribute('innerText'), \
                'page_source': temp, \
                'date': date})
            
            #关闭标签
            driver.close()
            driver.switch_to_window(driver.window_handles[0])

            time.sleep(0.5)

        try:
            elem = driver.find_element_by_xpath('//*[text()="下页"]')
            elem.click()
        except Exception as e:
            break

dir_part_one = make_dir('银监会机关')
dir_part_two = make_dir('银监局')
dir_part_three = make_dir('银监分局')


# driver = utils.ChromeBrowser()
# run(driver, dir_part_one, 'http://www.cbrc.gov.cn/chinese/home/docViewPage/110002.html')
# # run(driver, dir_part_two, 'http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//1.html')
# # run(driver, dir_part_three, 'http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//2.html')
# driver.quit()

def search(text, date_start, date_end):
    for item in my_set.find( {'$and': [ {'date': {'$gte': date_start, '$lt': date_end}}, \
        {'content':{'$regex': text}} \
        ] } ):

        print(item['name'])    

result = my_set.find({'content':{'$regex':"王凯"}})
print(result.count())
for item in result:
    print(item['name'])
    file_name = 'D:/IPA/external/search_result.html'
    with open(file_name, "w") as f:
        encoding = '<meta http-equiv="Content-Type" content="text/html; charset=gb2312">'
        f.write(encoding)
        f.write(item['page_source'].replace('黑体', '')) #.encode("gbk","ignore").decode("gbk"))
        break

# import pdfkit
# pdfkit.from_file('D:/IPA/external/search_result.html', 'search_result.pdf')

start = datetime.datetime(2018, 1, 1)
end = datetime.datetime(2018, 6, 1)
# a = my_set.find({'date': {'$gte': start, '$lt': end}})

# print(start)
# print(end)

# print(a.count())
# for item in my_set.find({'date': {'$gte': start, '$lt': end}}):
#     print(item['name'])

for item in my_set.find( {'$and': [ {'date': {'$gte': start, '$lt': end}}, \
    {'content':{'$regex':"中国银行保险监督管理委员会"}} \
    ] } ):

    print(item['name'])    