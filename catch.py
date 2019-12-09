#coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

# driver = webdriver.Firefox()
# url = "http://quote.cfi.cn/fhpx/19766/601985.html"
# driver.get(url)

# elem = driver.find_element_by_xpath("/html/body/form/table[1]/tbody/tr[2]/td[1]/div/div/div[16]/div[1]/nobr/font")
# elem.click()

# elem = driver.find_element_by_xpath('//*[@id="searchcode"]')
# elem.click()
# elem.send_keys('000001')
# elem.send_keys(Keys.RETURN)


def string2Float(str):
    try:
        result = float(str)
        return result
    except Exception as e:
        return 0

driver = webdriver.Firefox()
url = "http://quote.cfi.cn/stockList.aspx"
driver.get(url)

elem = driver.find_element_by_xpath('//*[@id="divcontent"]')
a_tags = elem.find_elements_by_xpath(".//a")

print(len(a_tags))

# 依次点击进入各个股票
for a_tag in a_tags:
    name = a_tag.get_attribute('innerText')

    a_tag.click()
    driver.switch_to_window(driver.window_handles[1])
    time.sleep(2)

    # 该股票最近的价格
    last = driver.find_element_by_xpath('//*[@id="last"]')
    temp = last.get_attribute('innerText')
    lastPrice = string2Float(temp[0:-1])
    print(name, ': 股票最近的价格 ', lastPrice)
    
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
            print('平均股息：', totalAmount / (i - 1) /  (lastPrice * 10))
            
    except Exception as e:
        print(e) 

    driver.close()
    driver.switch_to_window(driver.window_handles[0])
    print('-------------------------------------------------------')

