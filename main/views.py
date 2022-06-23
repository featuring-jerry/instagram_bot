from django.shortcuts import render

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys

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
search_keyword = "xx_veens"
first_post_atag_css= "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl _a6hd"

# 특정 게시물의 URL이 주어진 경우
specific_url_needs_to_likes_and_coments = "https://www.instagram.com/p/9Xdxr-MF4Z/"

# 특정채널
specific_channel = "https://www.instagram.com/xx_veens/"

def index(request):
    # login_type = ["facebook", "instagram"]
    login()
    time.sleep(7)

    trackUnfollower(specific_channel)
    time.sleep(99999)

    # 특정 게시물에 좋아요 / 댓글 달기 - 
    # url: "https://www.instagram.com/p/9Xdxr-MF4Z/"
    browser.get(specific_url_needs_to_likes_and_coments)
    time.sleep(3)
    clickLikeBtn()
    time.sleep(2)
    comment()

    # 인스타 메인화면 - 검색창 - "xx_veens"(채널이름)입력 - 첫 번째 채널 클릭 - 첫 번째 게시글 클릭 - 좋아요, 댓글달기
    search()
    clickLikeBtn()
    comment()

    time.sleep(99999)
    
    return render(request, 'main/index.html')

# 페이스북 로그인
def login():
    global browser
    # browser = wd.Chrome(executable_path=r"../instagram_venv/bin/chromedriver")
    browser = wd.Chrome(ChromeDriverManager().install())
    browser.implicitly_wait(2)
    browser.get(instagram_url)
    time.sleep(3)
    is_facebook_btn_click = False
    is_login_success = False

    try:
        facebook_login_btn = browser.find_element_by_css_selector(facebook_login_page_css)
        time.sleep(3)
        facebook_login_btn.click()
        is_facebook_btn_click = True
        is_login_success = True

    except:
        print("click facebook login button 1 fail")
        is_facebook_btn_click = False
        is_login_success = False

    time.sleep(3)

    if not is_facebook_btn_click:
        print("try click facebook login button 2")
        try:
            facebook_login_btn = browser.find_element_by_css_selector(facebook_login_page_css2)
            time.sleep(3)
            facebook_login_btn.click()
            is_facebook_btn_click = True
            is_login_success = True

        except:
            print("click facebook login button 2 fail")
            is_login_success = False
                
    time.sleep(3)

    id_input_form = browser.find_element_by_id(facebook_id_form_id)
    pw_input_form = browser.find_element_by_id(facebook_pw_form_id)

    id_input_form.send_keys(my_settings.user_id)
    pw_input_form.send_keys(my_settings.user_passwd)

    time.sleep(3)
    login_btn = browser.find_element_by_id(facebook_login_btn_css)
    login_btn.click()
    time.sleep(10)
    print("로그인이 정상적으로 완료되었습니다.")

    try:
        time.sleep(1)
        notnow = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[2]')
        notnow.click()
        print("접근권한 설정 나중에 하기 완료!")

    except:
        print("나중에 하기를 찾을 수 없어요!")

        try: 
            browser.get("https://instagram.com/official_jerry_superman")

        except:
            print("홈으로도 못가요!")

    # wait = ui.WebDriverWait(browser, 15)
    # a = wait.until(
    #     EC.text_to_be_present_in_element((By.CLASS_NAME, "_a9-- _a9_1"), '나중에 하기')
    # )
    # a.click()
    
    time.sleep(2)

    return

def search():
    try:
        search_input_form = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[2]/input")
    # search_input_form.focus()
        time.sleep(1)
        search_input_form.send_keys("xx_veens")
        time.sleep(4)
        first_search_target_channel = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a")
        first_search_target_channel.click()
        time.sleep(2)
        print("정상적으로 검색이 완료되었어요!")
    except:
        print("검색 실패로 인해 홈화면으로 갑니다.")
        browser.get("https://instagram.com")
        return


    try:
        first_post_element = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/div[3]/article/div/div/div[1]/div[1]/a")
        # second_post_element = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/div[3]/article/div/div/div[1]/div[2]/a")
        # first_post_element = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/div[3]/article/div/div/div[1]/div[3]/a")

        # first_post_element = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/div[3]/article/div/div/div[2]/div[1]/a")
        # first_post_element = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/div[3]/article/div/div/div[2]/div[2]/a")
        # first_post_element = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/div[3]/article/div/div/div[2]/div[3]/a")

        # first_post_element = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/div[3]/article/div/div/div[2]/div[1]/a")
        # first_post_element = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/div[3]/article/div/div/div[2]/div[1]/a")
        # first_post_element = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/div[3]/article/div/div/div[2]/div[1]/a")

        # adksljfaklsdfjdkla = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/div[3]/article/div/div/div[11]/div[2]/a")

        # first_post_element = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/div[3]/article/div/div/div[12]/div[2]/a")
        time.sleep(2)
        first_post_element.click()
        time.sleep(2)
        print("정상적으로 n번째 포스트에 들어왔어요!")
    except:
        print("n번째 포스트 입장에 실패로 인해 홈화면으로 갑니다.")
        browser.get("https://instagram.com")

    return


# 좋아요!
def clickLikeBtn():
    try:
        like_btn = browser.find_element_by_xpath("//span[@class='_aamw']/button")
        # like_btn = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button")
        time.sleep(2)
        like_btn.click()
        print("좋아요 버튼이 정상적으로 눌렸어요!")

    except:
        print("n번째 포스트 입장에 실패로 인해 홈화면으로 갑니다.")
        browser.get("https://instagram.com")

    return

# 댓글 달기!
def comment():
    try:
        activate_comment_btn = browser.find_element_by_xpath("//span[@class='_aamx']/button")
        # activate_comment_btn = browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[2]/button")
        activate_comment_btn.click()
        print("정상적으로 댓글창을 불러왔어요!")

    except:
        print("댓글창을 불러올 수 없거나 이미 활성화 되어있을지도?!")
    time.sleep(3)

    try:
        # textarea (댓글 입력공간) 특정하기
        comment_area = browser.find_element_by_xpath('//form[@class="_aao9"]/textarea')
        # comment_area = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/textarea')
        comment_area.click()
        time.sleep(3)

        # textarea에 댓글 입력
        comment_area.send_keys("잘 보고 가요~")
        time.sleep(3)

        # 댓글 추가 버튼 특정하기
        comment_add_btn = browser.find_element_by_xpath("//form[@class='_aao9']/button")
        # comment_add_btn = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/button')
        comment_add_btn.click()
        time.sleep(3)
        print("정상적으로 댓글이 남겨졌어요!")

    except:
        print("댓글남기기에 실패하여 메인으로 갑니다.")
        browser.get("https://instagram.com")

    return

def trackUnfollower(channel_url):

    # 1. 해당채널로 이동
    try:
        browser.get(channel_url)
        print("맞팔안한사람 트래킹할 채널로 들어왔습니다.")
    except:
        print("특정 채널을 찾을 수가 없어 메인으로 갑니다.")
        browser.get("https://instagram.com")
        return


    # 1-1. 팔로워 숫자 파악
    follower_number = int(browser.find_elements_by_xpath("//span [@class='_ac2a']")[1].text)
    print(follower_number, "팔로워 숫자")


    # 2. 팔로워 popup
    try:
        follower_popup_element = browser.find_element_by_xpath("//div[contains(text(),'팔로워 ')]/..")
        follower_popup_element.click()
        # browser.find_element_by_partial_link_text("팔로워 ").click()
        time.sleep(3)
        
    except:
        print("ㅋㅋ")
        browser.get("https://instagram.com")
        return

    # try:
    #     pop_up_window = ui.WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div[3]/div/button")))

    # except:
    #     print("실패했어요 ㅠㅠ")
    #     browser.get("https://instagram.com")
    #     return
    time.sleep(3)

    # last_height = browser.execute_script("return document.body.scrollHeight")
    # while True:
    #     # browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', pop_up_window)
    #     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(2)
    #     new_height = browser.execute_script("return document.body.scrollHeight")
    #     time.sleep(2)
    #     if new_height == last_height:
    #         break
    #     last_height = new_height
    # time.sleep(3)
    # ##
    # print("정상적으로 팔로워 창을 다 내렸어요!")
    # ##
    # scroll_box = browser.find_element_by_xpath("//div[@class='qg4pu3sx flebnqrf kzt5xp73 h98he7qt e793r6ar pi61vmqs od1n8kyl h6an9nv3 j4yusqav']")
    # followers_elements = browser.find_elements_by_class_name("_aacl _aaco _aacw _aacx _aad7 _aade")

    i = 0
    # 팔로워 숫자만큼 루프돔
    while(i < follower_number):
        element = browser.find_elements_by_xpath("//div[@role='dialog']//ul//li")
    # executing scroll into view script to view the element and thats gonna load the next element(follower ) ..ultimately your scrolling achived
        browser.execute_script("arguments[0].scrollIntoView(true);",element[i])
        print(i)
        i = i + 1
        time.sleep(0.8)
        if i % 10 == 0:
            time.sleep(3)

    followers_elements = browser.find_elements_by_class_name("_aacl _aaco _aacw _aacx _aad7 _aade")
    follower_list = []
    for follower in followers_elements:
        follower_list.append(follower.text)
    
    print(follower_list)
    return

    # //div[contains(text(),'팔로워 ')]/..
