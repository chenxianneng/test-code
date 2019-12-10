#coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from pymongo import MongoClient
import re

conn = MongoClient('localhost', 27017)
db = conn.mydb
my_set = db.shares

def string2Float(str):
    try:
        result = float(str)
        return result
    except Exception as e:
        return 0

driver = webdriver.Firefox()
url = "http://quote.cfi.cn/stockList.aspx"
driver.get(url)
driver.implicitly_wait(10)

elem = driver.find_element_by_xpath('//*[@id="divcontent"]')
a_tags = elem.find_elements_by_xpath(".//a")

print(len(a_tags))

# 依次点击进入各个股票
for a_tag in a_tags:
    name = a_tag.get_attribute('innerText')

    a_tag.click()
    driver.switch_to_window(driver.window_handles[1])
    # time.sleep(2)

    try:
        # 该股票最近的价格
        last = driver.find_element_by_xpath('//*[@id="last"]')
        temp = last.get_attribute('innerText')
        lastPrice = string2Float(temp[0:-1])
        print(name, ': 当前股价 ', lastPrice)
        # 股票详细信息
        infos_table = driver.find_element_by_xpath('//*[@id="quotetab_stock"]')
        # 市盈率
        elem = infos_table.find_element_by_xpath('.//tbody/tr[3]/td[1]')
        pe = elem.get_attribute('innerText')
        print('市盈率：', pe)
        # 市净率
        elem = infos_table.find_element_by_xpath('.//tbody/tr[4]/td[1]')
        pb = elem.get_attribute('innerText')
        print('市净率：', pb)
        # 振幅
        elem = infos_table.find_element_by_xpath('.//tbody/tr[1]/td[3]')
        wave = elem.get_attribute('innerText')
        print(wave)
        # 换手率
        elem = infos_table.find_element_by_xpath('.//tbody/tr[1]/td[4]')
        switchRate = elem.get_attribute('innerText')
        print(switchRate)   
        # 成交量     
        elem = infos_table.find_element_by_xpath('.//tbody/tr[2]/td[3]')
        volume = elem.get_attribute('innerText')
        print(volume)
        # 成交额
        elem = infos_table.find_element_by_xpath('.//tbody/tr[2]/td[4]')
        Turnover = elem.get_attribute('innerText')
        print(Turnover) 
        # 总市值         

        # 选择分红派息
        temp = driver.find_element_by_xpath('//*[@id="nodea26"]')
        temp.click()

        # 历年的分红表
        table = driver.find_element_by_xpath('//*[@id="tabh"]')
        rows = table.find_elements_by_xpath('.//tr')
        # print(len(rows))

        values = []

        totalAmount = 0.0
        i = 0

        try:
            for row in rows:
                if i != 0:
                    elem = row.find_element_by_xpath('.//td[7]')
                    value = elem.get_attribute('innerText')
                    # print(value)
                    values.append(value)
                    totalAmount += string2Float(value)
                i += 1

            if i > 1 and lastPrice > 1:
                # 打印股息    
                averageRate = totalAmount / ((i - 1) / 2) /  (lastPrice * 10)
                print('平均每10股派发分红：', round(totalAmount / ((i - 1) / 2), 2), '元    平均分红利率：', round(averageRate * 100, 2), '%')

                # 市盈率
                result = re.findall("\d+\.\d+", pe)
                if len(result) > 0:
                    pe = result[0]
                else:
                    pe = 0.0

                # 市净率
                result = re.findall("\d+\.\d+", pb)
                if len(result) > 0:
                    pb = result[0]
                else:
                    pb = 0.0

                # 振幅
                result = re.findall("\d+\.\d+", wave)
                if len(result) > 0:
                    wave = result[0]
                else:
                    wave = 0.0                
                # 换手率
                result = re.findall("\d+\.\d+", switchRate)
                if len(result) > 0:
                    switchRate = result[0]
                else:
                    switchRate = 0.0                   
                # 成交量
                result = re.findall("\d+", volume)
                if len(result) > 0:
                    volume = result[0]
                else:
                    volume = 0.0                   
                # 成交额
                result = re.findall("\d+\.\d+", Turnover)
                if len(result) > 0:
                    Turnover = result[0]
                else:
                    Turnover = 0.0            

                # 把结果插入数据库
                my_set.insert({'name': name, \
                '最新股价': lastPrice, \
                '分红利率': round(averageRate, 4), \
                '平均每10股派发分红': round(totalAmount / ((i - 1) / 2), 2), \
                '振幅': string2Float(wave), \
                '换手率': string2Float(switchRate), \
                '成交量': string2Float(wave), \
                '成交额': string2Float(Turnover), \
                '市盈率': string2Float(pe), \
                '市净率': string2Float(pb)})           
        except Exception as e:
            print(e) 

    except Exception as e:   
        print(e)  
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
        print('-------------------------------------------------------------------------------------')
        continue

    driver.close()
    driver.switch_to_window(driver.window_handles[0])
    print('-------------------------------------------------------------------------------------')