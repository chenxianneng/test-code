#coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import utils
import time
import os
import datetime
from pymongo import MongoClient
import pdfkit

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
        
def catch_data(driver, url, limit_date=None , browser='chrome'):    
    driver.get(url)
    #driver.maximize_window()
    driver.implicitly_wait(10)
    
    while True:
        elem = driver.find_element_by_xpath('//*[@id="testUI"]')
        #elem.find_elements_by_xpath('')
        #trs = elem.find_elements_by_xpath(".//a")
        a_tags = elem.find_elements_by_xpath(".//a[@class='STYLE8']")
        print(len(a_tags))
        try:
            for a_tag in a_tags:
                parent = a_tag.find_element_by_xpath('..')
                record_date = parent.find_element_by_xpath("following::td")
                temp = record_date.get_attribute('innerText').split('-')
                # print(temp)
                
                date = datetime.datetime(int(temp[0]), int(temp[1]), int(temp[2]))

                if limit_date is not None and stop_catche(limit_date, record_date):
                    driver.quit()
                    return
                
                
                title = a_tag.get_attribute('title')
                temp = my_set.find({"name": title})
                if temp.count() != 0:
                    continue

                print(title)
                a_tag.click()    

                #选择标签
                driver.switch_to_window(driver.window_handles[1])

                content = driver.page_source
                #page_source = content.encode("gbk","ignore").decode("gbk")
                
                content_elem = driver.find_element_by_class_name('n_cent')
                temp = content_elem.get_attribute('innerHTML') #.encode("gbk","ignore").decode("gbk")

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
        except Exception as e:
            print(e)

    return True

def run():
    driver = utils.ChromeBrowser()
    try:
        catch_data(driver, 'http://www.cbrc.gov.cn/chinese/home/docViewPage/110002.html')
        catch_data(driver, 'http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//1.html')
        catch_data(driver, 'http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//2.html')
        driver.quit()
    except Exception as e:
        driver.quit()
        print('发生异常等待5秒自动重新调用函数.......')
        time.sleep(5)
        run()

def search(text, start, end, page_index, record_count):
    options = {
                'page-size': 'Letter',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'custom-header': [
                    ('Accept-Encoding', 'gzip')
                ],
                'cookie': [
                    ('cookie-name1', 'cookie-value1'),
                    ('cookie-name2', 'cookie-value2'),
                ],
                'outline-depth': 10,
            }

    temp = start.split('-')
    date_start = datetime.datetime(int(temp[0]), int(temp[1]), int(temp[2]))
    temp = end.split('-')
    date_end = datetime.datetime(int(temp[0]), int(temp[1]), int(temp[2]))

    # file_name = utils.get_working_dir() + '/search_result.html'
    search_result = temp = my_set.find( {'$and': [ {'date': {'$gte': date_start, '$lt': date_end}}, \
        {'content':{'$regex': text}} \
        ] } )

    if page_index > 1:
        search_result = temp.skip(page_index * record_count).limit(record_count)
    else:
        search_result = temp.limit(record_count)

    pdf_list = []
    dir_pdf = make_dir('search_result')
    result_string = '<meta charset="UTF-8">'
    for item in search_result:
        # result_string = '<meta charset="UTF-8">'
        print(item['name'])
        result_string += item['page_source'].replace('黑体', '')

    print('siting size: ', len(result_string))
    pdf_path = dir_pdf + item['name'] + '.pdf'
    pdfkit.from_string(result_string, pdf_path, options=options)
    download_path = 'http://localhost:8080/cbrc/search_result/' + str(time.time()) + '.pdf'
    pdf_list.append(download_path)

    amount = math.ceil(temp.count() / record_count)
    
    return amount, pdf_list

if __name__ == '__main__':
    # dir_part_one = make_dir('银监会机关')
    # dir_part_two = make_dir('银监局')
    # dir_part_three = make_dir('银监分局')


    run()

    a = search('王凯', '2016-1-1', '2019-12-31', 1, 10)
    print(a)