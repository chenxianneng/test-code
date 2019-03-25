
import subprocess
import os
import logging
import random
from threading import Thread
from multiprocessing import Process
from time import sleep, localtime, strftime
import copy
import uiautomator2 as u2

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(filename)s - line:%(lineno)d - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s')


def stop_wechat(device):
    device.app_stop('com.tencent.mm')

def start_wechat(device):
    # 启动微信
    output, exit_code = device.shell("am start -n com.tencent.mm/com.tencent.mm.ui.LauncherUI", timeout=60)
    # print(output, exit_code)

def add_contact_friend(device, word=''):
        
    stop_wechat(device)
    start_wechat(device)
    
    sleep(3)



    start_time = localtime()

    handler = logging.FileHandler(device.device_info['serial'] + ".log")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # device(resourceId="com.tencent.mm:id/d3t").click(timeout=5)
    try:
        device(text='通讯录').click(timeout=5)
        b = device(text='通讯录')
        print(b.info)
        device(text='新的朋友').click(timeout=3)
    except Exception as e:
        logger.info('无法进入通讯录')
        return
    logger.info('%s %s', device.device_info['serial'], 'start')
    contactname = ""

    count, total, no_confirm, newcount = 0, 0, 0, 0 # count = 1 跳过第一个空tag
    firstendloop = True
    try:
        while True:
        

            brn = device(resourceId="com.tencent.mm:id/btk")
            newcount = brn.count-1
            newcount1 = brn.count
            if newcount1 <= 0:
                break
            if count >= newcount1:
                device(scrollable=True).scroll(100)     # 下一屏幕
                sleep(2.0)
                count = 1

            mynum = brn[count].child().count-1
            if  brn[count].child().count < 5:
               count += 1
               continue

            record, status = brn[count].child()[0].child(), brn[count].child()[1].child()
            nickname, owner1 = record[0], record[1].info['text']
            print(count, nickname.info['text'], owner1, status.info['text'])
            owner = copy.deepcopy(owner1)
            if status.info['text'] == "等待验证" or status.info['text'] == "已添加" :
                count += 1
                total += 1
                if count == newcount1:  # 在最后爬取
                    if firstendloop:
                        firstendloop = False
                        contactname = copy.deepcopy(owner)
                    else:
                        if contactname == owner:
                             break
                        else:
                            firstendloop = True
                continue
            # 进入联系人页面
            nickname.click()

            if device(text="添加到通讯录").wait(timeout=3):
                try:
                    device(text="添加到通讯录").click()
                except Exception as e:
                    logger.error(str(e) + "tongxunlu")
                    sleep(3)
                    device(text="添加到通讯录").click()
                # 等待页面刷新
                sleep(2.0)

                try:
                    last_name = owner[10]
                except Exception as e:
                    last_name = owner[6:]
                words = last_name + word
                print(words)

                #device(resourceId="com.tencent.mm:id/e0o").wait()

                try:
                    greeting = device(resourceId="com.tencent.mm:id/e0o")
                    greeting.send_keys(words)
                except Exception as e:
                    logger.error(str(e)+"send_keys(")
                    try:
                        device(text="确定").click()
                    except Exception as e:
                        logger.error(str(e)+"确定errrr")
                    device.press("back")
                    count += 1
                    total += 1
                    if count == newcount1:  # 在最后爬取
                        if firstendloop:
                            firstendloop = False
                            contactname = copy.deepcopy(owner)
                        else:
                            if contactname == owner:
                                break
                            else:
                                firstendloop = True
                    continue
                device(text="发送").wait(timeout=5)
                btn_5 = device(text='发送')
                btn_5.click()

                try:
                    device(resourceId="com.tencent.mm:id/kb").click()
                    sleep(1)
                    if device(text="添加到通讯录"):
                        device(resourceId="com.tencent.mm:id/kb").click()
                except Exception as e:
                    logger.error(str(e) + "return")
                    sleep(4)
                    device(resourceId="com.tencent.mm:id/kb").click()
                # 等待页面刷新
                #sleep(2.5)
                #device.press("back")
                device(resourceId="com.tencent.mm:id/btk")[count].child()[1].child().click()   #点击添加
                #status.click()       #点击添加
            else:
                no_confirm += 1
                sleep(3)
                device.press("back")
                device(resourceId="com.tencent.mm:id/btk")[count].child()[1].child().click()  # 点击添加
                sleep(3)
                device.press("back")
                logger.warning('%s %d %d', '无验证用户', no_confirm, count)
        
            
            count += 1
            total += 1
            logger.info('%s 送出邀请%d条 无验证%d条', owner, total, no_confirm)
            interval = random.randint(1, 5)
            print(interval)
            sleep(interval)
            if count == newcount1:          #在最后爬取
                if firstendloop:
                    firstendloop = False
                    contactname = copy.deepcopy(owner)
                else:
                    if contactname == owner:
                        break
                    else:
                        firstendloop = True

    except Exception as e:
        logger.error(str(e))

    end = localtime()
    logger.info('%s %s', strftime("%a %b/%d/%Y %H:%M:%S", start_time), strftime("%a %b/%d/%Y %H:%M:%S", end))
        

def get_page_hierarchy(device):
    xml = device.dump_hierarchy()
    with open('dump3.xml', 'w', encoding='utf-8') as f:
        f.write(xml)
    # d.toast.show("Hello world")


if __name__ == '__main__':

    word = '总,我是微众银行客户经理小婷,祝您新春大吉!现我行提供无抵押、低利率的企业贷款服务,欢迎详询!'
    cmd = 'adb devices'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    outs, errs = proc.communicate(timeout=15)

    device_list = outs.decode().split()[4:][0::2]
    print(device_list)
    cmd2 = 'python -m uiautomator2 init '
    for serial_num in device_list:
         proc = subprocess.Popen(cmd2 + '--serial ' + serial_num + ' ', shell=True, stdout=subprocess.PIPE)
         outs, errs = proc.communicate(timeout=15)
    # d = u2.connect(device_list[0])

    # d.implicitly_wait(5.0)
    # get_page_hierarchy(d)
    # add_contact_friend(d, 10, word)

    l = []
    for serial_num in device_list:
         dev = u2.connect(serial_num)
         dev.implicitly_wait(3.0)
         print(dev.device_info)
         p = Thread(target=add_contact_friend, args=(dev, word, ), daemon=False)
    #     # p = Process(target=add_contact_friend, args=(dev, 400, word, ), daemon=False)
         l.append(p)
        
    for p in l:
         p.start()

    

    