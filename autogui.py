from pyautogui import *
from humancursor import *
import darkerdb
import pyautogui
import time
import keyboard
import numpy as np
import random
import win32api, win32con


time.sleep(1)

def lerp(t, a, b):
    return ((1 - t) * a) + (t * b)

#clicks at x and y coordiantes in (pixels?) OLD
'''
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    click_delay = random.uniform(.10, .40)
    print(f"click delay: {click_delay}")
    time.sleep(click_delay)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
'''

def human_type(text):
    for char in text:
        pyautogui.write(char)
        time.sleep(random.uniform(.05, .2))

def click_type_tester():
    cursor.click_on([500,300])
    human_type("antdraw is Hella sexcy!")



#selects marketplace item and enters name, selecting item
#should prob take all item attributes but for now will just take name
def select_item(item_name):
    #hard coded "select item" pixel pos
    cursor.click_on([137, 205])
    human_type(item_name)
    

cursor = SystemCursor()
#select item
#cursor.move_to([137, 205])

click_type_tester()