from django.shortcuts import render

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import my_settings
import time
import re
import json
import pandas as pd

facebook_login_page_css = ".sqdOP.yWX7d.y3zKF     "
facebook_login_page_css2 = ".sqdOP.L3NKy.y3zKF     "
facebook_id_form_id = "email"
facebook_pw_form_id="pass"
facebook_login_btn_css="loginbutton"

url = "https://www.instagram.com/p/CRQAQ02Lpyq/"
instagram_url = 'https://www.instagram.com/'

# 상태: 로그인 된 상태
landing_setting_alarms_css = "_a9-- _a9_1"
_login_search_input_css = "_aawh _aawj _aauy"
search_keyword = "xx_veens"
first_post_atag_css= "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl _a6hd"

# global browser

def index(request):
    # login_type = ["facebook", "instagram"]
    login()
    # browser.get(instagram_url)
    time.sleep(7)
    # parent_h = browser.current_window_handle
    # handles = browser.window_handles
    # handles.remove(parent_h)
    # browser.switch_to.window(handles.pop())
    # set_alarm_btn = browser.find_element_by_css_selector(landing_setting_alarms_css)
    # time.sleep(6)
    # set_alarm_btn.click()
    # time.sleep(7)
    # browser.switch_to.window(parent_h)
    browser.find_element_by_xpath("//button[contains(text(), '나중에 하기')]").click()


    # try:
    #     alert = browser.switch_to_alert()
    #     time.sleep(2)
    #     print(alert.text)
    #     alert.dismiss()
    # except:
    #     print("There is no alert")

    time.sleep(8)
    search()

    clickLikeBtn()

    time.sleep(99999)
    
    

    return render(request, 'main/index.html')

# 페이스북 로그인
def login():
    global browser
    browser = wd.Chrome(executable_path=r"../instagram_venv/bin/chromedriver")
    browser.implicitly_wait(2)
    browser.get(instagram_url)
    time.sleep(3)
    is_facebook_btn_click = False
    is_login_success = False

    try:
        facebook_login_btn = browser.find_element_by_css_selector(facebook_login_page_css)
        time.sleep(6)
        facebook_login_btn.click()
        is_facebook_btn_click = True
        is_login_success = True
    except:
        print("click facebook login button 1 fail")
        is_facebook_btn_click = False
        is_login_success = False

    time.sleep(4)

    if not is_facebook_btn_click:
        print("try click facebook login button 2")
        try:
            facebook_login_btn = browser.find_element_by_css_selector(facebook_login_page_css2)
            time.sleep(5)
            facebook_login_btn.click()
            is_facebook_btn_click = True
            is_login_success = True
        except:
            print("click facebook login button 2 fail")
            is_login_success = False
                
    time.sleep(10)

    id_input_form = browser.find_element_by_id(facebook_id_form_id)
    pw_input_form = browser.find_element_by_id(facebook_pw_form_id)

    id_input_form.send_keys(my_settings.user_id)
    pw_input_form.send_keys(my_settings.user_passwd)

    time.sleep(6)

    login_btn = browser.find_element_by_id(facebook_login_btn_css)

    login_btn.click()
    return
    
    # username_input = browser.find_element_by_css_selector("input[name='username']")
    # password_input = browser.find_element_by_css_selector("input[name='password']")

    # username_input.send_keys(my_settings.user_id)
    # password_input.send_keys(my_settings.user_passwd)

    # login_button = browser.find_element_by_xpath("//button[@type='submit']")
    # login_button.click()
    

    # browser.close()
    # return

def search():
    search_input_form = browser.find_element_by_css_selector(_login_search_input_css)
    time.sleep(7)
    search_input_form.send_keys(search_keyword)
    time.sleep(5)
    search_input_form.submit()
    time.sleep(7)
    first_post_element = browser.find_element_by_css_selector(first_post_atag_css)
    time.sleep(4)
    first_post_element.click()
    return

def clickLikeBtn():
    like_btn = browser.find_element_by_css_selector("_abl-")
    time.sleep(3)
    like_btn.click()
    return