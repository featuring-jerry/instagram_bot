from django.shortcuts import render

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys

from main.instagram_crawler import InstagramBot
import random
import my_settings
import time
import re
import json
import pandas as pd

# import multiprocessing
from main.models import DirectMessage

facebook_login_page_css = ".sqdOP.yWX7d.y3zKF     "
facebook_login_page_css2 = ".sqdOP.L3NKy.y3zKF     "
facebook_id_form_id = "email"
facebook_pw_form_id="pass"
facebook_login_btn_css="loginbutton"

url = "https://www.instagram.com/p/CRQAQ02Lpyq/"
instagram_url = 'https://www.instagram.com/'

# 상태: 로그인 된 상태
landing_setting_alarms_css = "_a9-- _a9_1"
search_keyword = "yyongjoon"
first_post_atag_css= "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl _a6hd"

# 특정 게시물의 URL이 주어진 경우
specific_url_needs_to_likes_and_coments = "https://www.instagram.com/p/9Xdxr-MF4Z/"

# 특정채널
specific_channel = "https://www.instagram.com/cob_202103/"

# Moons
# channel_id = 'super_moon_1999'
# channel_id = 'cob_202103'


def index(request):
    # channel_list = ['super_moon_1999', 'cob_202103', 'wookdw']
    # pool = multiprocessing.Pool(processes=3)
    # pool.map()

    # for i in range(3):
    #     thread = InstagramBot(my_settings.user_id, my_settings.user_passwd, name="insta_bot {}".format(i))
    #     thread.start()
    #     thread.logIn()
    #     thread.setPermisson()
    #     thread.DM("super_moon_1999", "THREADING ADOPTED: This is Jerry's msg for testing Insagram_bot dev version2")
    # time.sleep(99999)
    print(DirectMessage.objects.filter()[0].message)
    time.sleep(99999)
    insta_bot1 = InstagramBot(my_settings.user_id, my_settings.user_passwd)
    insta_bot1.log_in()
    insta_bot1.set_permisson()

    # insta_bot1.search("cob_202103")

    #### DM 보내기 ####
    insta_bot1.direct_message("wookdw", "Hey wook, this is Jerry's msg by Instagram_bot dev_1 version!")
    time.sleep(99999)


    ## 좋아요 댓글 남기기
    # 1. 특정 포스트로 이동
    post_url = "https://www.instagram.com/p/Ccb0N72pHb7/"
    insta_bot1.enter_post(post_url)

    # 2. 좋아요 버튼
    insta_bot1.click_like_btn()

    # 3. 댓글 남기기
    content = "우와 된장술밥 정말 맛있겠네요! 오늘 한번 도전해봐야겠어요!"
    insta_bot1.comment(content)

    ## 팔로우 - 팔로워 트래킹 (불필요 기능인듯)
    """
    trackUnfollower(specific_channel)
    time.sleep(99999)
    """

    time.sleep(99999)
    
    return render(request, 'main/index.html')

def testMulti():
    insta_bot = 1
    return


def trackUnfollower(channel_url):
    browser = wd.Chrome(ChromeDriverManager().install())
    # 1. 해당채널로 이동
    try:
        browser.get(channel_url)
        print("맞팔안한사람 트래킹할 채널로 들어왔습니다.")
    except:
        print("특정 채널을 찾을 수가 없어 메인으로 갑니다.")
        browser.get("https://instagram.com")
        return

    # 1-0. 비공개 채널일 때 분기처리
    try:
        private_channel_check = browser.find_element_by_xpath("//div[@class='_aa_t']")
        print("비공개 채널이라서 분석이 불가능합니다, 팔로우 요청을 하거나 채널의 주인이라면 공개채널로 전환 후 시도해주세요.")
        print("종료합니다.")
        browser.close()
    except:
        print("비공개 계정이 아닙니다!")
    
    # 1-1. 팔로워 숫자 파악
    # follower_number = int(browser.find_elements_by_xpath("//span [@class='_ac2a']")[1].text)
    follower_number = int(browser.find_element_by_xpath("//div [contains(text(), '팔로워 ')]/span").text.replace(",", ""))
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
        time.sleep(3)
        return

    # try:
    #     pop_up_window = ui.WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div[3]/div/button")))

    # except:
    #     print("실패했어요 ㅠㅠ")
    #     browser.get("https://instagram.com")
    #     return
    

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

    pop_up_window = ui.WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='_aano']")))

    for i in range(int(follower_number/4)):
        browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pop_up_window)
        time.sleep(random.randrange(500,1000) / 1000)

    # while(i < follower_number):
    #     browser.execute_script(
    #     'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', pop_up_window)

    #     browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pop_up_window)
    #     i = i + 1
    #     time.sleep(0.3)
        
        

    #     listed_followers_element = browser.find_elements_by_css_selector('._aaey > div > li')
    #     if i >= len(listed_followers_element):
    #         break
    
        # try:
        #     element = browser.find_elements_by_xpath("//div[@role='dialog']//ul//li")
        #     browser.execute_script("arguments[0].scrollIntoView(true);",element[i])
        #     print(i)
        #     i = i + 1
        #     time.sleep(0.5)
        #     if i % 12 == 0:
        #         time.sleep(3)
        # except:
        #     break
    ul_element = browser.find_element_by_xpath("//ul[@class='_aaey']")
    # print(ul_element, "ul이요")

    followers_elements = ul_element.find_elements(By.XPATH, "//span[@class='_aacl _aaco _aacw _aacx _aad7 _aade']")
    # followers_elements = ul_element.find_elements(By.CLASS_NAME, "_aacl _aaco _aacw _aacx _aad7 _aade")
    # followers_elements2 = browser.find_elements_by_class_name("_aacl _aaco _aacw _aacx _aad7 _aade")

    # followers_elements3 = browser.find_elements_by_css_selector('._aaey > div > li')
    # followers_elements4 = ul_element.find_elements(By.CSS_SELECTOR, '._aaey > div > li')

    # print(followers_elements)
    # print(followers_elements2)
    # print(followers_elements3)
    # print(followers_elements)

    follower_list = []
    # follwer_list2 = []
    for follower in followers_elements:
        follower_list.append(follower.get_attribute('innerText'))
        # follwer_list2.append(follower.text)
    
    # print("팔로워들의 리스트에요!", follower_list)
    # print(follwer_list2)

    # 차집합을 구하기 위해 set 활용
    follower_list = set(follower_list)


    # 팝업창 닫기
    try:
        close_btn_element = browser.find_element(By.XPATH, "//div[@class='_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p  _ab9y']/button")
        close_btn_element.click()
        print("닫기 버튼을 눌렀어요!")
    except:
        browser.get(channel_url)
        print("닫기 버튼을 못찾아서 그냥 타겟 채널로 갑니다 ㅠ")


    ####################################################################################################################################################################################

    # 팔로우 리스트 가져오기
    # 1-1. 팔로우 숫자 파악
    follow_number = int(browser.find_element_by_xpath("//div [contains(text(), '팔로우 ')]/span").text)
    print(follow_number, "팔로우 숫자")


    # 2. 팔로우 popup
    try:
        follow_popup_element = browser.find_element_by_xpath("//div[contains(text(),'팔로우 ')]/..")
        follow_popup_element.click()
        time.sleep(3)
        
    except:
        browser.get("https://instagram.com")
        time.sleep(3)
        return
    

    pop_up_window2 = ui.WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='_aano']")))

    for i in range(int(follow_number/4)):
        browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pop_up_window2)
        time.sleep(random.randrange(500,1000) / 1000)

    ul_element = browser.find_element_by_xpath("//ul[@class='_aaey']")

    follow_elements = ul_element.find_elements(By.XPATH, "//span[@class='_aacl _aaco _aacw _aacx _aad7 _aade']")

    follow_list = []
    
    for follow in follow_elements:
        follow_list.append(follow.get_attribute('innerText'))

    # 차집합을 구하기 위해 set 활용
    follow_list = set(follow_list)

    ####################################################################################################################################################################################

    bad_guy_list = follow_list - follower_list
    print("나는 팔로우하고있는데 팔로잉 안해준 bad guy list를 출력합니다!")
    print(bad_guy_list)


    return 

    # //div[contains(text(),'팔로워 ')]/..