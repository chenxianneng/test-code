#!/usr/bin/env python


import json
import csv
import time
import os
import logging

from urllib.request import Request, urlopen,quote
from inspect import isfunction

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(filename)s - line:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s')
handler = logging.FileHandler("log.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

#构造获取经纬度的函数
def getlnglat(address):
    logger.info('地理位置获取中...')
    url = 'http://api.map.baidu.com/geocoder/v2/?address='
    output = 'json'
    ak = 'OGIX9IqXvqM8LRDHhmVAPlGpFlkd4gf8'
    add = quote(address)    #本文城市变量为中文，为防止乱码，先用quote进行编码
    url2 = url+add+'&output='+output+"&ak="+ak
    req = Request(url2)
    req.set_proxy('10.106.234.92:9090', 'http')
    res  = urlopen(req).read().decode()
    temp = json.loads(res)
    logger.info('地理位置获取完毕...')
    return temp

def get_working_dir():
    dirname = os.path.dirname(__file__)
    return dirname

'''
Browser activities
'''
def ChromeBrowser():
    '''
    Opens the Chrome/IE Browser in a Selenium instance.

    Returns:
        webdriver: Selenium Webdriver

    '''
    dirname = os.path.dirname(__file__)
    chrome_path = 'src/drivers/chromedriver.exe'
    filename = os.path.join(dirname, chrome_path)

    directory = get_working_dir() + "/tax_report/"
    options = webdriver.ChromeOptions() 
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': directory}
    options.add_experimental_option('prefs', prefs) 
        
    return webdriver.Chrome(executable_path=filename, options=options)

def IeBrowser():
    
    dirname = os.path.dirname(__file__)
    ie_path = 'src/drivers/IEDriverServer_32.exe'
    filename = os.path.join(dirname, ie_path)    
    return webdriver.Ie(filename)

if __name__ == '__main__':
    pass