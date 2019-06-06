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

def catch_data(driver, url, table_tag, browser='chrome'):  
    driver.get(url)
    # driver.maximize_window()
    driver.implicitly_wait(10)

    while True:
        # elem = driver.find_element_by_xpath('//table[@id="ess_ctr14430_ModuleContent"]')
        elem = driver.find_element_by_xpath(table_tag)
        trs = elem.find_elements_by_xpath('.//a[@target="_blank"]')
        print(len(trs))
        try:
            for tr in trs:
                title = tr.get_attribute('title')
                print(title)
                temp = my_set.find({"name": title})
                if temp.count() != 0:
                    continue

                tr.click()
                #点击进入执行信息
                #webdriver.ActionChains(driver).move_to_element(elem).click(elem).perform()
                parent = tr.find_element_by_xpath('..')
                record_date = parent.find_element_by_xpath("following::td")
                temp = record_date.get_attribute('innerText').replace('(', '').replace(')', '').split('-')
                # print(temp)

                date = datetime.datetime(int('20' + temp[0]), int(temp[1]), int(temp[2]))

                #选择标签
                driver.switch_to_window(driver.window_handles[1])
                # content = driver.page_source

                content_elem = driver.find_element_by_id('tab_content')
                temp = content_elem.get_attribute('innerHTML')

                my_set.insert({'name':title, \
                    'content':content_elem.get_attribute('innerText'), \
                    'page_source':temp, \
                    'date': date})

                #关闭标签
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
                time.sleep(1)
        except Exception as e:
            print(e)

        elem = driver.find_element_by_link_text("下一页")
        href = elem.get_attribute('href')
        if href is not None:
            elem.click()
        else:
            break
            
    return True

def search(text, date_start, date_end):
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

    result_string = '<meta charset="UTF-8">'
    for item in my_set.find( {'$and': [ {'date': {'$gte': date_start, '$lt': date_end}}, \
        {'content':{'$regex': text}} \
        ] } ):

        result_string += item['page_source'].replace('黑体', '')
   
    print('siting size: ', len(result_string))
    pdf_path = 'result.pdf'
    pdfkit.from_string(result_string, pdf_path, options=options)

    return pdf_path

def run():
    driver = utils.ChromeBrowser()
    try:
        catch_data(driver, 'http://bxjg.circ.gov.cn/web/site0/tab5240/', '//table[@id="ess_ctr14430_ModuleContent"]')
        catch_data(driver, 'http://bxjg.circ.gov.cn/web/site0/tab5241/', '//table[@id="ess_ctr14458_ListC_Info_LstC_Info"]')
        driver.quit()
    except Exception as e:
        driver.quit()
        print('发生异常等待5秒自动重新调用函数.......')
        time.sleep(5)
        run()

if __name__ == '__main__':
    # dir_part_one = make_dir('保监会处罚')
    # dir_part_two = make_dir('保监局处罚')

    # driver = utils.ChromeBrowser()
    # catch_data(driver, 'http://bxjg.circ.gov.cn/web/site0/tab5240/', '//table[@id="ess_ctr14430_ModuleContent"]')
    # catch_data(driver, 'http://bxjg.circ.gov.cn/web/site0/tab5241/', '//table[@id="ess_ctr14458_ListC_Info_LstC_Info"]')
    # driver.quit()

    run()

    start = datetime.datetime(2018, 1, 1)
    end = datetime.datetime(2019, 12, 1)

    search("杨帆", start, end)