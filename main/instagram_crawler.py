from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import random
import re
import json
import pandas as pd

import time
import os
import sys
# from dateutil.tz import gettz

from datetime import datetime, timezone, timedelta
from functools import partial, update_wrapper, WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES

# import threading

from main.models import InstagramChannel, ChannelPost, ChannelStatistics

random_hashtag = ["#햄버거", "#피자", "#선릉맛집"]
class InstagramBot:
    # 생성자 - 로그파일 생성
    def __init__(self, user_id, user_pw):
        
        # threading.Thread.__init__(self)
        # self.name = name
        # today = str(date.today())

        KST = timezone(timedelta(hours=9))
        time_record = datetime.now(KST)
        today = str(time_record)[:10]

        if not(os.path.isdir(today)):
            os.mkdir(os.path.join(today))

        sys.stdout = open('{today}/stdout.txt'.format(today=today), 'a')

        self.user_id = user_id
        self.user_pw = user_pw
        # self.browser = wd.Chrome(ChromeDriverManager().install())
        self.browser = wd.Chrome(executable_path=r"../instagram_venv/bin/chromedriver")

        self.instagram_url = "https://www.instagram.com/"

    # 소멸자 - 소멸시에 로그파일을 닫아준다.
    def __del__(self):
        sys.stdout.close()


    def timer(func):
    # decorator function
        def wrapper(*args, **kwargs):
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], func, "함수 시작")
            ret = func(*args, **kwargs)
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], func, "함수 끝")
            return ret
        wrapped = partial(update_wrapper, wrapped=func, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)
        return wrapped(wrapper)


    @timer
    def log_in(self):
    # 페이스북 아이디로 로그인하기
        self.browser.implicitly_wait(2)
        self.browser.get(self.instagram_url)

        # facebook_login_page_css = ".sqdOP.yWX7d.y3zKF     "
        # facebook_login_page_css2 = ".sqdOP.L3NKy.y3zKF     "
        facebook_login_page_css3 = ".sqdOP yWX7d    y3zKF     "
        
        # is_facebook_btn_click = False
        # is_login_success = False




        try:
            # facebook_login_btn = self.browser.find_element_by_css_selector(facebook_login_page_css)
            time.sleep(2)

            facebook_login_btn = ui.WebDriverWait(self.browser, random.random() + 3).until(EC.visibility_of_element_located("//span[(text()='Facebook으로 로그인')]/../../button"))
            facebook_login_btn.click()
            time.sleep(random.random() + 1)
            # is_facebook_btn_click = not is_facebook_btn_click
            # is_login_success = not is_login_success

        except:
            print("2번 실패")
            time.sleep(2)


        try:
            time.sleep(2)
            factbook_btn = self.browser.find_element_by_xpath("//span[(text()='Facebook으로 로그인')]/../../button")
            factbook_btn.click()
        except:
            print("1번 실패")

        try:
            facebtn = self.browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[5]/button")
            facebtn.click()

        except:
            print("3번 실패")
            time.sleep(1)

        try:

            face4 = self.browser.find_element_by_css_selector(facebook_login_page_css3)
            face4.click()

        except:
            print("4번 실패")
            time.sleep(9999)

        # if not is_facebook_btn_click:
        #     print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "try click facebook login button 2")
        #     try:
        #         facebook_login_btn = self.browser.find_element_by_css_selector(facebook_login_page_css2)
        #         facebook_login_btn.click()
        #         time.sleep(random.random() + 1)
        #         is_facebook_btn_click = not is_facebook_btn_click
        #         is_login_success = not is_login_success

        #     except:
        #         print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "click facebook login button 2 fail")

        time.sleep(random.random() + 2)

        id_input_form = self.browser.find_element_by_id("email")
        pw_input_form = self.browser.find_element_by_id("pass")

        id_input_form.send_keys(self.user_id)
        time.sleep(random.random())
        pw_input_form.send_keys(self.user_pw)
        time.sleep(random.random())

        login_btn = self.browser.find_element_by_id("loginbutton")
        login_btn.click()
        print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "로그인이 정상적으로 완료되었습니다.")
        time.sleep(random.random() + 11)

        return


    @timer
    def set_permisson(self):
    # 로그인 시 나타나는 설정-나중에하기 popup창 처리
        try:
            # notnow = ui.WebDriverWait(self.browser, random.random() + 5).until(EC.element_located_to_be_selected(By.XPATH,"//button[contains(text(), '나중에 하기')]"))
            notnow = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[2]')
            notnow.click()
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "권한 설정 나중에 하기 완료!")

        except:
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "권한 설정 - 나중에 하기를 찾을 수 없어요!")
            self.browser.close()

        return


    @timer
    def search(self, channel_id):
    # 검색창에 특정 채널 id 검색해서 해당 채널로 이동
        try:
            # search_input_form = self.browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[2]/input")
            search_input_form = self.browser.find_element_by_xpath("//input[contains(@placeholder, '검색')]")
            search_input_form.send_keys(channel_id)
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "{channel_id} 인스타그램 채널을 검색합니다!".format(channel_id=channel_id))

            time.sleep(random.random() + 4)

            # first_search_target_channel = ui.WebDriverWait(self.browser, random.random() + 1).until(EC.element_to_be_clickable(By.XPATH, "//a[contains(@href,'/{channel_id}/')]".format(channel_id=channel_id)))
            first_search_target_channel = self.browser.find_element_by_xpath("//a[contains(@href,'/{channel_id}/')]".format(channel_id=channel_id))
            first_search_target_channel.click()
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "정상적으로 검색이 완료되었어요!")

            time.sleep(random.random() + 4)

            #####django 저장
            if InstagramChannel.objects.filter(channel_id=channel_id).exists() == False:
                channel_url = "https://www.instagram.com/{channel_id}/".format(channel_id=channel_id)
                print(channel_url)
                channel_thumbnail = self.browser.find_element_by_xpath("//img [contains(@alt, '{channel_id}님의 프로필 사진')]".format(channel_id=channel_id)).get_attribute('src')
                print(channel_thumbnail)
                InstagramChannel(channel_id=channel_id, channel_url=channel_url, channel_thumbnail=channel_thumbnail).save()


        except:
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "검색 실패로 인해 브라우저를 종료합니다.")
            self.browser.close()

        return
    

    @timer
    def enter_post(self, target_post_url): # url로 받는게 나을 것 같음
    # 해당 게시물로 이동 - 없는 url이면 에러없이 홈화면으로 가지기 때문에 만듦
        # target_post_url = self.instagram_url + "/p/" + post_id + "/"

        self.browser.get(target_post_url)

        if target_post_url != self.browser.current_url:
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "해당 게시물을 찾을 수 없어서 브라우저를 종료합니다.")
            self.browser.close()
            return
        
        print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "정상적으로 게시글에 들어왔습니다.")
        return


    # clickLikeBtn(), comment() - 게시글 안에 들어와 있을 때

    @timer
    def click_like_btn(self):
    # (해당포스트에 들어와있을 때 사용가능) 따봉버튼 누르기
        try:
            like_btn = ui.WebDriverWait(self.browser, random.random() + 2).until(EC.element_to_be_clickable("//span[@class='_aamw']/button"))
            like_btn.click()
            time.sleep(random.random() + 1)
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "좋아요 버튼이 정상적으로 눌렸어요!")

        except:
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "게시글 입장에 실패로 인해 브라우저를 종료합니다.")
            self.browser.close()

        return
    

    @timer
    def comment(self, content):
    # (해당포스트에 들어와있을 때 사용가능) 댓글달기
        try:
            activate_comment_btn = ui.WebDriverWait(self.browser, random.random() + 3).until(EC.element_to_be_clickable("//span[@class='_aamx']/button"))
            activate_comment_btn.click()
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "정상적으로 댓글창을 불러왔어요!")
        
        except:
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "댓글창을 불러올 수 없거나 이미 활성화 되어있을지도?!")
        
        try:
            # 댓글창
            comment_area = ui.WebDriverWait(self.browser, random.random() + 2).until(EC.element_to_be_clickable("//form[@class='_aao9']/textarea"))
            comment_area.click()
            time.sleep(random.random() + 1)
            comment_area.send_keys(content)

            # 댓글 등록 버튼
            comment_add_btn = ui.WebDriverWait(self.browser, random.random() + 1).until(EC.element_to_be_clickable("//form[@class='_aao9']/button"))
            comment_add_btn.click()
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "정상적으로 댓글이 남겨졌어요!")
            time.sleep(random.random() + 3)

        except:
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "댓글남기기에 실패하여 메인으로 갑니다.")
            self.browser.get("https://instagram.com")

        return



    @timer
    def activate_specific_channel_dm(self, channel_id):
    # 메인에서 특정채널 검색해서 들어간다음에 메시지보내기 버튼 클릭
        
        # 1. 특정채널 검색해서 들어가기
        self.search(channel_id)

        # 2. 메시지 보내기 버튼 클릭
        check_if_succes = False
        try:
            send_message_button_element = ui.WebDriverWait(self.browser, 2).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'메시지 보내기')]/..")))
            send_message_button_element.click()
            check_if_succes = not check_if_succes
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "메시지 보내기 버튼 클릭에 성공했어요!")
        
        except:
            try:
                print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "메시지 보내기 버튼 클릭에 실패하여 follow요청 후 DM을 재시도 합니다!")
                follow_button_element = self.browser.find_element_by_xpath("//h2[contains(text(), 'wookdw')]/..//div[contains(text(), '팔로우')]")
                follow_button_element.click()
                send_message_button_element = ui.WebDriverWait(self.browser, 3).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'메시지 보내기')]/..")))
                send_message_button_element.click()
                check_if_succes = not check_if_succes
                print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "메시지 보내기 버튼 클릭에 성공했어요!")

            except:
                print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "메시지 보내기 버튼 클릭에 실패했어요!")
                print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "랜딩 페이지로 돌아갑니다.")
                self.browser.get(self.instagram_url)

        return check_if_succes


    # (DM창 안에 있을 때 사용가능) DM 보내기  cf) 조합된 function - DM(self, ...) 을 사용하세요!
    @timer
    def send_dm(self, message):
        try:
            textarea_element = ui.WebDriverWait(self.browser, 3).until(EC.visibility_of_element_located((By.XPATH, "//textarea[contains(@placeholder,'메시지 입력...')]")))
            textarea_element.click()
            time.sleep(random.random() + 1)
            textarea_element.send_keys(message)
            textarea_element.send_keys(Keys.ENTER)
            
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "DM을 성공적으로 전송했습니다.")

        except:
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "DM 메시지 창에 도착했으나 DM보내기에 실패했어요!")
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "랜딩 페이지로 돌아갑니다.")
            self.browser.get(self.instagram_url)
    
        return


    ############################### 조합된 function ##################################

    @timer
    def direct_message(self, channel_id, message):
        """ # DM(channel_id, message)
            # input값 2가지:
            # (1) channel_id - DM보낼 채널명
            # (2) message - 전달할 DM 메시지 내용
            # ex) instabot("official_jerry_superman", "제리님 팬이에요~!")

            # 함수 시작: 메인에서 시작
            # 함수 기능: 메인에서 채널 검색 후, 채널에서 메시지보내기 누르고, DM 화면들어가서 DM 보내기
        """
        print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "{channel_id} 채널에 '{message}' 메세지 보내기를 시작합니다!".format(channel_id=channel_id, message=message))
        is_valid_channel = self.activate_specific_channel_dm(channel_id)

        if is_valid_channel:
            self.send_dm(message)

        return


    @timer
    def likes_with_comment(self, target_url, content):
        """# likesWithComment(target_url, content)
        # input값 2가지:
        # (1) target_url - 해당 포스트의 full url
        # (2) content - 댓글내용
        # ex) likesWithComment("https://www.instagram.com/p/Ccb0N72pHb7/", "우와 된장술밥 정말 맛있겠네요! 오늘 한번 도전해봐야겠어요!")

        # 함수 시작: anywhere
        # 함수 기능: target_url에 해당하는 포스트에 따봉과 댓글을 남긴다.
        """
        print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "{target_url} 에 따봉과 {content} 를 남깁니다!".format(target_url=target_url, content=content))
        self.enter_post(target_url)
        self.click_like_btn()
        self.comment(content)
        return

    @timer
    def random_acts_to_dm(self, channel_id, message, level):
    # 결국 할 행위는 DM 보내기 / 1~10 사이의 수준을 입력하면 그의 합당한 랜덤행위하다가 DM보냄. 
        if type(level) != int:
            print("level은 1~10 사이의 정수로 입력해주세요!")
            self.browser.close()
            return
        if level < 0 or level > 10:
            print("level은 1~10 사이의 정수로 입력해주세요!")
            self.browser.close()
            return
        
        
        random_hashtag[random.randint(0,2)]

        self.direct_message(channel_id, message)
        return


    @timer
    def hangout_1(self, level):
    # hangout_1: 랜덤 해쉬태그 검색 및 포스트 서핑
        if level <= 0:
            return
        for i in range(1,level):
            pop_up_window = ui.WebDriverWait(self.browser, 2).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='_abnx']")))
            self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;", pop_up_window)
            time.sleep(random.randrange(500,1000) / 1000)
            return

        return
    
    # 해쉬태그 검색헤서 들어가기까지, keyword는 스트링이며, #이 추가되어있는 스트링이다.
    def search_hashtag(self, keyword):
        
        try:
            search_input_form = self.browser.find_element_by_xpath("//input[contains(@placeholder, '검색')]")
            search_input_form.send_keys(keyword)
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "{keyword} 해쉬태그를 검색합니다!".format(keyword=keyword))

            time.sleep(random.random() + 4)
            # //div[contains(text()[1],'#') and text()[2] = '피자']
            # //div[contains(text()[1],'#') and text()[2] = '피자']/../../../../..
            first_search_target_channel = self.browser.find_element_by_xpath("//div[contains(text()[1],'#') and text()[2]='{keyword}')/../../../../..]".format(keyword=keyword[1:]))
            first_search_target_channel.click()
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "정상적으로 검색이 완료되었어요!")

            time.sleep(random.random() + 4)

        except:
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "검색 실패로 인해 브라우저를 종료합니다.")
            self.browser.close()
        return
        

# TODO: 
# 인스타그램 행위 - 해쉬태그검색, 좋아요, 댓글, 팔로워, 언팔로워, 팔로우, DM, id검색
# - 브라우저 행위로 이루어짐.
# - 행위를 여러가지로(될때까지):
# 1차 & 2차 행위로 나누고, Random 하게,
# 
# 행위, 횟수, 시간, ...., 
# 슬랙에 공유 회의 주제, 회의 내용, 회의 수준, 데드라인 - 슬랙 업무 공유 


# 브라우징 행위 (클릭, 스크롤, 뒤로가기, 타이핑 ...)
