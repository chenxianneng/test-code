#-*- coding:utf-8 -*-
from pynput.mouse import Listener as Mouse_Listener
from pynput.keyboard import Key
from pynput.keyboard import Listener as Keyboard_Listener
import pickle
import threading
import time

from pynput.mouse import Button

print(Button.left)

lock = threading.Lock()
record = []
stop = False
mouse_listen_thread = None
keyboard_listen_thread = None

def on_move(x, y):
    # 监听鼠标移动
    print('Pointer moved to {0}'.format((x, y)))

def on_click(x, y, button, pressed):
    global record

    # 监听鼠标点击
    msg = {}
    msg['type'] = 'mouse'
    msg['x'] = x
    msg['y'] = y
    msg['button'] = button
    if pressed:
        msg['action'] = 'press'
    else:
        msg['action'] = 'release'

    lock.acquire()
    record.append(msg)
    lock.release()
    
    print('{0} at {1} {2}'.format('Pressed' if pressed else 'Released', (x, y), button))

def on_scroll(x, y, dx, dy):
    # 监听鼠标滚轮
    print('Scrolled {0}'.format((x, y)))

def on_press(key):
    global record
    
    msg = {}
    msg['type'] = 'keyboard'
    msg['key'] = key
    msg['action'] = 'press'

    lock.acquire()
    record.append(msg)
    lock.release()
    
    # 监听按键
    print('{0} pressed'.format(key))

def on_release(key):
    global record
    
    msg = {}
    msg['type'] = 'keyboard'
    msg['key'] = key
    msg['action'] = 'release'

    lock.acquire()
    record.append(msg)
    lock.release()
    
    # 监听释放
    print('{0} release'.format(key))
    if key == Key.esc:
        #print(record)
        pickle.dump(record, open("record.p", "wb"))
        
        keyboard_listen_thread.stop()
        mouse_listen_thread.stop()
        #return False

def start_record():
    global record
    global keyboard_listen_thread
    global mouse_listen_thread

    record.clear()

    # 连接事件以及释放
    mouse_listen_thread = Mouse_Listener(on_click=on_click, on_scroll=on_scroll)
    mouse_listen_thread.start()

    # 连接事件以及释放
    keyboard_listen_thread = Keyboard_Listener(on_press=on_press, on_release=on_release)
    keyboard_listen_thread.start()

def repeat_one_time():
    from pynput.mouse import Button
    from pynput.mouse import Controller as Mouse_Controller
    from pynput.keyboard import Controller as Keyboard_Controller

    mouse = Mouse_Controller()
    keyboard = Keyboard_Controller()
    
    record_data = pickle.load(open("record.p", "rb"))
    print(record_data)
    
    for action in record_data:
        if action['type'] == 'mouse':
            mouse.position = (int(action['x']), int(action['y']))
            if action['action'] == 'press':
                mouse.press(action['button'])
            elif action['action'] == 'release':
                mouse.release(action['button'])
        elif action['type'] == 'keyboard':
            if action['action'] == 'release':
                keyboard.release(action['key'])
            elif action['action'] == 'press':
                keyboard.press(action['key'])

        time.sleep(0.1)
            
#start_record()

repeat_one_time()
