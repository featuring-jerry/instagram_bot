from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

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

random_hashtag = ["#햄버거", "#피자", "#선릉맛집", "#수지", "#우기"]


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
        self.browser = wd.Chrome(ChromeDriverManager().install())
        # self.browser = wd.Chrome(executable_path=r"../instagram_venv/bin/chromedriver")

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


    # 페이스북 아이디로 로그인하기
    @timer
    def log_in(self):
        self.browser.implicitly_wait(3)
        self.browser.get(self.instagram_url)

        try:
            facebook_login_btn = ui.WebDriverWait(self.browser, random.random() + 20).until(EC.visibility_of_element_located((By.XPATH, "//span[(text()='Facebook으로 로그인')]/../../button")))
            facebook_login_btn.click()
            time.sleep(random.random() + 1)
        except:
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "Facebook으로 로그인 버튼을 찾을 수 가 없습니다. 종료합니다.")
            self.browser.quit()

        ui.WebDriverWait(self.browser, random.random() + 20).until(EC.visibility_of_all_elements_located((By.ID, "email")))

        id_input_form = self.browser.find_element(By.ID, "email")
        pw_input_form = self.browser.find_element(By.ID, "pass")

        id_input_form.send_keys(self.user_id)
        time.sleep(random.random())
        pw_input_form.send_keys(self.user_pw)
        time.sleep(random.random())

        login_btn = self.browser.find_element(By.ID, "loginbutton")
        login_btn.click()
        time.sleep(random.randint(2,4))
        print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "로그인이 정상적으로 완료되었습니다.")

        return


    @timer
    def set_permisson(self):
    # 로그인 시 나타나는 설정-나중에하기 popup창 처리
        try:
            notnow = ui.WebDriverWait(self.browser, random.random() + 20).until(EC.visibility_of_element_located((By.XPATH,"//button[contains(text(), '나중에 하기')]")))
            # notnow = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[2]')
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
            search_input_form = self.browser.find_element(By.XPATH, "//input[contains(@placeholder, '검색')]")
            search_input_form.clear()
            search_input_form.send_keys(channel_id)
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "{channel_id} 인스타그램 채널을 검색합니다!".format(channel_id=channel_id))

            time.sleep(random.random() + 4)

            first_search_target_channel = ui.WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/{channel_id}/')]".format(channel_id=channel_id))))
            # first_search_target_channel = self.browser.find_element(By.XPATH, "//a[contains(@href,'/{channel_id}/')]".format(channel_id=channel_id))
            first_search_target_channel.click()
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "정상적으로 검색이 완료되었어요!")

            time.sleep(random.random() + 4)

            #####django 저장
            if InstagramChannel.objects.filter(channel_id=channel_id).exists() == False:
                channel_url = "https://www.instagram.com/{channel_id}/".format(channel_id=channel_id)
                # print(channel_url)
                channel_thumbnail = self.browser.find_element(By.XPATH, "//img [contains(@alt, '{channel_id}님의 프로필 사진')]".format(channel_id=channel_id)).get_attribute('src')
                # print(channel_thumbnail)
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
            like_btn = ui.WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='_aamw']/button")))
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
            activate_comment_btn = ui.WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH ,"//span[@class='_aamx']/button")))
            activate_comment_btn.click()
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "정상적으로 댓글창을 불러왔어요!")
        
        except:
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "댓글창을 불러올 수 없거나 이미 활성화 되어있을지도?!")
        
        try:
            # 댓글창
            comment_area = ui.WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH ,"//form[@class='_aao9']/textarea")))
            comment_area.click()
            time.sleep(random.random() + 1)
            comment_area.send_keys(content)

            # 댓글 등록 버튼
            comment_add_btn = ui.WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH ,"//form[@class='_aao9']/button")))
            comment_add_btn.click()
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "정상적으로 댓글이 남겨졌어요!")
            time.sleep(random.random() + 3)

        except:
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "댓글남기기에 실패하여 메인으로 갑니다.")
            self.browser.get("https://instagram.com")

        return



    # 메인에서 특정채널 검색해서 들어간다음에 메시지보내기 버튼 클릭
    @timer
    def activate_specific_channel_dm(self, channel_id):
        
        # 1. 특정채널 검색해서 들어가기
        self.search(channel_id)

        # 2. 메시지 보내기 버튼 클릭
        check_if_succes = False
        try:
            send_message_button_element = ui.WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'메시지 보내기')]/..")))
            send_message_button_element.click()
            check_if_succes = not check_if_succes
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "메시지 보내기 버튼 클릭에 성공했어요!")
        
        except:
            try:
                print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "메시지 보내기 버튼 클릭에 실패하여 follow요청 후 DM을 재시도 합니다!")
                follow_button_element = self.browser.find_element(By.XPATH, "//h2[contains(text(), 'wookdw')]/..//div[contains(text(), '팔로우')]")
                follow_button_element.click()
                send_message_button_element = ui.WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'메시지 보내기')]/..")))
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
            textarea_element = ui.WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//textarea[contains(@placeholder,'메시지 입력...')]")))
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

    def scroll_down_on_search(self, level):
        if level <= 0:
            print("<func: scroll_down_on_search>, 레벨은 1이상이어야 합니다.")
            return
        print("level = {level}".format(level=level))
        start = time.time()
        pop_up_window = ui.WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='_abnx']")))
        for i in range(60):
            self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 120", pop_up_window)
            time.sleep(random.random() * level)

        print("time : ", time.time() - start)

        # if level == 10:
        #     pop_up_window = ui.WebDriverWait(self.browser, 2).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='_abnx']")))
        #     self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;", pop_up_window)

        return

    @timer
    def hangout_1(self, level):
    # hangout_1: 랜덤 해쉬태그 검색 및 포스트 서핑
        if level <= 0:
            return
        for i in range(1,level):
            
            

            return

        return
    

    ############ Random acts ###################### Random acts ###################### Random acts ###################### Random acts ########################
    # 놀다가 나오는 곳은 꼭 검색이 가능한곳이어야 한다. (포스트 안에서 X)
    # 주의 hash_lst 길이보다 level 이 길면 안됨 (현재 - level 1이상 5이하만 됨)
    def random_hashtag_play(self, hash_lst, level, scroll_level): 
        hash_lst.append(1) ## tmp
        
        for i in range(1, level):
            random_number = random.randint(0, len(random_hashtag) - 1)
            target_hashtag = random_hashtag[random_number]
            del random_hashtag[random_number]
            self.search_hashtag(target_hashtag, scroll_level)
        self.browser.get("https://www.naver.com")
        time.sleep(10)
        return

    # 해쉬태그 검색헤서 들어가기까지, keyword는 스트링이며, #이 추가되어있는 스트링이다.
    def search_hashtag(self, keyword, scroll_level):
        
        try:
            search_input_form = self.browser.find_element(By.XPATH, "//input[contains(@placeholder, '검색')]")
            search_input_form.send_keys(Keys.RETURN)
            search_input_form.send_keys(keyword)
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "{keyword} 해쉬태그를 검색합니다!".format(keyword=keyword))
            self.scroll_down_on_search(scroll_level)
            time.sleep(random.random() + 4)
            # //div[contains(text()[1],'#') and text()[2] = '피자']
            # //div[contains(text()[1],'#') and text()[2] = '피자']/../../../../..
            first_search_target_channel = ui.WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text()[1], '#') and text()[2]='{keyword}']/../../../../..".format(keyword=keyword[1:]))))
            # first_search_target_channel = self.browser.find_element(By.XPATH, "//div[contains(text()[1],'#') and text()[2]='{keyword}')/../../../../..]".format(keyword=keyword[1:]))
            first_search_target_channel.click()
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "정상적으로 검색이 완료되었어요!")

            time.sleep(random.random() + 4)

        except:
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "검색 실패로 인해 브라우저를 종료합니다.")
            self.browser.close()

        return
    
class InstagramHangoutBot:
    def __init__(self, user_id, user_pw, login_by):
        KST = timezone(timedelta(hours=9))
        time_record = datetime.now(KST)
        today = str(time_record)[:10]

        if not(os.path.isdir(today)):
            os.mkdir(os.path.join(today))

        sys.stdout = open('{today}/stdout.txt'.format(today=today), 'a')

        
        self.user_id = user_id
        self.user_pw = user_pw
        self.login_by = login_by

        chrome_options = wd.ChromeOptions()
        chrome_options.add_argument("--incognito")


        self.browser = wd.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
        self.mission = []
        self.instagram_url = "https://www.instagram.com/"

    # 소멸자 - 소멸시에 로그파일을 닫아준다.
    def __del__(self):
        sys.stdout.close()
    
    # decorator function
    def timer(func):
        def wrapper(*args, **kwargs):
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], func, "함수 시작")
            ret = func(*args, **kwargs)
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], func, "함수 끝")
            return ret
        wrapped = partial(update_wrapper, wrapped=func, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)
        return wrapped(wrapper)

    @timer
    def log_in(self):
        def facebook_login():
            try:
                facebook_login_btn = ui.WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//span[(text()='Facebook으로 로그인')]/../../button")))
                facebook_login_btn.click()
                time.sleep(random.random() + 1)
            except:
                print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "Facebook으로 로그인 버튼을 찾을 수 가 없습니다. 종료합니다.")
                self.browser.quit()
            ui.WebDriverWait(self.browser, random.random() + 10).until(EC.visibility_of_all_elements_located((By.ID, "email")))

            id_input_form = self.browser.find_element(By.ID, "email")
            pw_input_form = self.browser.find_element(By.ID, "pass")

            id_input_form.send_keys(self.user_id)
            time.sleep(random.random())
            pw_input_form.send_keys(self.user_pw)
            time.sleep(random.random())

            login_btn = self.browser.find_element(By.ID, "loginbutton")
            login_btn.click()
            time.sleep(random.randint(2,4))
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "로그인이 정상적으로 완료되었습니다.")

            return
        def instagram_login():
            id_input_elem = ui.WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//input [@name='username']")))
            pw_input_elem = self.browser.find_element(By.XPATH, "//input [@name='password']")
            id_input_elem.send_keys(self.user_id)
            time.sleep(random.randrange(2,3))
            pw_input_elem.send_keys(self.user_pw)
            time.sleep(random.randrange(1,2))

            login_btn_elem = self.browser.find_element(By.XPATH,"//div [contains(text(), '로그인')]/..")
            login_btn_elem.click()
            time.sleep(random.randint(2,3) + 2)
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "로그인이 정상적으로 완료되었습니다.")
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "참고: 인스타그램 로그인은 나중에 하기를 2번 눌러요!")
            self.set_permisson()

            return

        self.browser.implicitly_wait(4)
        self.browser.get(self.instagram_url)

        if self.login_by == "facebook":
            return facebook_login()

        return instagram_login()

    @timer
    def set_permisson(self):
    # 로그인 시 나타나는 설정-나중에하기 popup창 처리
        try:
            time.sleep(random.random()+ 5)
            notnow = ui.WebDriverWait(self.browser, random.random() + 20).until(EC.visibility_of_element_located((By.XPATH,"//button[contains(text(), '나중에 하기')]")))
            notnow.click()
            time.sleep(random.randint(2,3))
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "권한 설정 나중에 하기 완료!")

        except:
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "권한 설정 - 나중에 하기를 찾을 수 없어요!")
            self.browser.close()

        return

    @timer
    def get_current_url(self):
        return self.browser.current_url
    
    @timer
    def check_search_form_exist(self):
        try:
            self.browser.find_element(By.XPATH, "//input[contains(@placeholder, '검색')]")
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "검색 창이 존재하는 url 입니다.")
        except:
            return False
        
        return True

    @timer
    def random_activity(self):
        try:
            # 오류 페이지로 들어갔을 시 메인 페이지로 보냄
            self.browser.find_element(By.XPATH, "//h2 [contains(text(),'죄송합니다. 페이지를 사용할 수 없습니다.')]")
            return self.browser.get(self.instagram_url)
        except:
            pass
        
        print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "random activity를 시작합니다.")
        time.sleep(random.random() + 5)
        # ui.WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//div [@class='_aagw']")))
        current_url = self.get_current_url()
        url_state = self.get_where_am_i(current_url)
        print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], current_url, "에서", url_state, "루틴을 시작합니다.")
        if url_state == 'main':
            return self.main_routine()
        elif url_state == 'post':
            return self.post_routine()
        elif url_state == 'dm':
            self.browser.get(self.instagram_url)
            time.sleep(random.random() + 2)
            return
        elif url_state == 'hashtag':
            return self.hashtag_routine()

        return

    @timer
    def main_routine(self):

        def scroll_down():
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "메인루틴 - scroll_down을 실행합니다")

            time.sleep(2 + random.randrange(2,3))
            # pop_up_window = ui.WebDriverWait(self.browser, 2).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/section/div/div[2]/div[1]/div")))
            ui.WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//article")))
            rand = random.randrange(15,60)
            for i in range(rand):
                self.browser.execute_script("window.scrollTo(window.scrollY, window.scrollY + Math.random((document.body.scrollHeight - window.scrollY) * 0.07, (document.body.scrollHeight - window.scrollY) * 0.1) * 550)")
                time.sleep(random.random() * 1.5)
                # self.browser.execute_script("window.scrollTo(windiw.scrollY, window.scrollY + Math.random((document.body.scrollHeight - window.scrollY) * 0.05, (document.body.scrollHeight - window.scrollY) * 0.1))")
                # self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 200", pop_up_window)
                # self.browser.execute_script("")
            func_list = [scroll_down, search, choose_post, explore_behavior]
            # func_list = [scroll_down, choose_post]
            random.choice(func_list[1:])()
            return
        
        def search():
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "메인루틴 - search_hashtag를 실행합니다")

            def scroll_down_on_search():
                print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "search_scroll_down을 실행합니다")
                # pop_up_window = ui.WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='_abnx']")))
                pop_up_window = ui.WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder, '검색')]/following-sibling::div/div/div/following-sibling::div/div")))
                random_number = random.randrange(15,35)
                time.sleep(random.random())
                for i in range(random_number):
                    # self.browser.execute_script("window.scrollTo(Math.random(document.body.scrollHeight - window.scrollY * 0.05, document.body.scrollHeight - window.scrollY * 0.1))")
                    self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + Math.random() * 40 + 90", pop_up_window)
                    time.sleep(random.random() + 0.5)

                return

            try:
                keyword = random.choice(["#피자", "#햄버거", "#아이스크림", "#카페", "#수지", "#뷰티", "#화장품", "#비비크림", "#왁싱", "#브라질리언왁싱", "#패션", "#일상", "#우기", "#카리나", "#영화", "#강아지", "#고양이", "#계곡", "#수영", "#여름", "#캠핑"])
                search_input_form = self.browser.find_element(By.XPATH, "//input[contains(@placeholder, '검색')]")
                search_input_form.clear()
                search_input_form.send_keys(keyword)
                print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "{keyword} 해쉬태그를 검색합니다!".format(keyword=keyword))
                scroll_down_on_search()
                time.sleep(random.random() * 2 + 1)
                # random_search_target_channel = ui.WebDriverWait(self.browser, random.random() + 4).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text()[1], '#') and contains(text()[2],'{keyword}')]/../../../../..".format(keyword=keyword[1:]))))
                random_search_target_channels = self.browser.find_elements(By.XPATH, "//div[contains(text()[1], '#') and contains(text()[2],'{keyword}')]/../../../../..".format(keyword=keyword[1:]))
                random_search_target_channel = random_search_target_channels[random.randrange(0, len(random_search_target_channels))]

                random_search_target_channel.click()
                print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "정상적으로 검색이 완료되었어요!")

                time.sleep(random.random() + 3)
                # self.browser.get(self.instagram_url)
                # TODO: 해시태그 루틴 구현해서 연결

            except:
                print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "검색 실패로 인해 직접 키워드 해쉬태그 url에 진입합니다.")
                self.browser.get(self.instagram_url + "explore/tags/{keyword}/".format(keyword=keyword[1:]))

            return

        def choose_post():
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "main에서 choose_post을  실행합니다")
            time.sleep(random.random() + 2)
            target_comment_btn_element = self.browser.find_element(By.XPATH, "//time [@class = '_aaqe']")
            actions = ActionChains(self.browser)
            actions.move_to_element(target_comment_btn_element)
            actions.click(on_element=target_comment_btn_element)
            actions.perform()
            time.sleep(random.random() + 2)

            # self.post_routine()

            return
        
        def explore_behavior():
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "explore_behavior을 실행합니다")
            time.sleep(random.randrange(2,3))
            explore_btn_element = self.browser.find_element(By.XPATH, "//*[local-name()='svg' and @aria-label='사람 찾기']/..")
            explore_btn_element.click()
            time.sleep(random.randrange(1,3) + 1)
            return
        print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "main_routine을 실행합니다")
        time.sleep(random.random() + 1)
        try:
            ui.WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div [@class='_aagw']")))
            func_list = [choose_post, scroll_down, search, explore_behavior]
            # func_list = [scroll_down]
            random.choice(func_list[1:])()
        except:
            explore_behavior()
            time.sleep(random.random() + 2)

        return

    @timer
    def post_routine(self):
        def check_next_button_and_click():
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "이미지 넘기기를 실행합니다.")
            time.sleep(random.random() * 2 + 0.8)
            image_count = 1
            while(True):
                try:
                    next_btn_elem = self.browser.find_element(By.XPATH, "//button [@class = ' _aahi']")
                    next_btn_elem.click()
                    time.sleep(random.random() * 3)
                    image_count += 1

                except:
                    while image_count > 1:
                        prev_btn_elem = self.browser.find_element(By.XPATH, "//button [@class = ' _aahh']")
                        prev_btn_elem.click()
                        time.sleep(random.random() * 3)
                        image_count -= 1
                    break
            if random.random() > 0.4:
                return random.choice([click_like_btn, scroll_down_comment])()
            # func_list = [click_like_btn]
            # return random.choice(func_list[1:])()
            return self.browser.get(self.instagram_url)

        def click_like_btn():
        # (해당포스트에 들어와있을 때 사용가능) 따봉버튼 누르기
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "좋아요 버튼 누르기를 post에서 실행합니다")
            # 해당 게시물이 이미 따봉 눌려있으면 걍 안한다.
            time.sleep(random.random() + 2)
            try:
                check_already_clicked = self.browser.find_element(By.XPATH, "//span[@class='_aamw']//* [local-name()='svg']").get_attribute("aria-label")
                if check_already_clicked == '좋아요 취소':
                    print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "이미 좋아요를 누른 게시물입니다.")
                    return
            except:
                print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "좋아요 aria-label을 get 할 수 없습니다.")
            

            try:
                like_btn = ui.WebDriverWait(self.browser, random.random() + 20).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='_aamw']/button")))
                like_btn.click()
                time.sleep(random.random() + 1)
                print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "좋아요 버튼이 정상적으로 눌렸어요!")
                self.browser.get(self.instagram_url)
                time.sleep(random.random() + 2)
            except:
                print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "좋아요 누르기 오류로 인해 브라우저를 종료합니다.")
                self.browser.close()

            return
        
        def scroll_down_comment():
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "post_scroll_down을 post에서 실행합니다")
            time.sleep(random.randrange(2,3))
            pop_up_window = self.browser.find_element(By.XPATH, "//ul [@class='_a9z6 _a9za']")
            random_number = random.randrange(6, 15)
            for i in range(random_number):
                random_scroll_height = random.randrange(50, 100)
                self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + {random_scroll_height}".format(random_scroll_height=random_scroll_height), pop_up_window)
                time.sleep(random.random() * 3)
                is_reached_bottom = self.browser.execute_script("return arguments[0].scrollTop + 200 >= arguments[0].scrollHeight;", pop_up_window)
                if is_reached_bottom:
                    break
                
            if random.random() > 0.4:
                return random.choice([click_like_btn, check_next_button_and_click])()
            return self.browser.get(self.instagram_url)

        ui.WebDriverWait(self.browser, random.random() + 20).until(EC.visibility_of_element_located((By.XPATH, "//span[@class='_aamw']/button")))
        # ui.WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "article")))
        print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "post_routine을 실행합니다")
        # func_list = [check_next_button_and_click, click_like_btn, scroll_down_comment]
        func_list = [check_next_button_and_click, click_like_btn, scroll_down_comment]
        random.choice(func_list)()

        return

    @timer
    def hashtag_routine(self):
        def scroll_down():
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "hashtag_routine - scroll_down을 실행합니다")

            time.sleep(3 + random.random())
            # pop_up_window = ui.WebDriverWait(self.browser, 2).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/section/div/div[2]/div[1]/div")))
            
            rand = random.randrange(30, 50)
            for i in range(rand):
                original_height = self.browser.execute_script("return document.documentElement.scrollTop;")
                self.browser.execute_script("window.scrollTo(window.scrollY, window.scrollY += Math.random((document.body.scrollHeight - window.scrollY) * 0.07, (document.body.scrollHeight - window.scrollY) * 0.1) * 540)")
                time.sleep(random.random() * 2)
                # self.browser.execute_script("window.scrollTo(windiw.scrollY, window.scrollY + Math.random((document.body.scrollHeight - window.scrollY) * 0.05, (document.body.scrollHeight - window.scrollY) * 0.1))")
                # self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 200", pop_up_window)
                # self.browser.execute_script("")
                changed_height = self.browser.execute_script("return document.documentElement.scrollTop;")
                if original_height + 200 >= changed_height:
                    break

            if random.random() > 0.9:
                time.sleep(random.random() * 3 + 2)
                self.browser.get(self.instagram_url)
                time.sleep(random.random() + 2)
                return
            
            if random.random() > 0.7 and self.get_current_url() == "https://www.instagram.com/explore/":
                print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], self.get_current_url() + "에서 새로고침을 합니다!")
                # print(self.get_current_url() + "에서 새로고침을 합니다!")
                self.browser.refresh()
                time.sleep(random.random() + 2)
                return

            time.sleep(random.random() + 2)
            return
        
        def choose_post():
            print("choose_post을 hashtag_routine에서 실행합니다")
            time.sleep(random.randint(1,3) + 2)
            
            # target_comment_btn_element = self.browser.find_element(By.XPATH, "//div [contains(@class,'_ac7v _aang')]/div/a")
            if self.get_current_url() == "https://www.instagram.com/explore/":
                # 해시태그 채널이아니라 나침반임
                print("나침반에서 choose_post 를 실행합니다.")
                ui.WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div [contains(@class,'_aagu')]/..")))
                ranged_element = self.browser.find_elements(By.XPATH, "//div [contains(@class,'_aagu')]/..")
            else:
                print("#해시태그 채널에서 choose_post 를 실행합니다.")
                ui.WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div [contains(@class,'_ac7v _aang')]/div/a")))
                ranged_element = self.browser.find_elements(By.XPATH, "//div [contains(@class,'_ac7v _aang')]/div/a")
            time.sleep(random.random() + 1)
            random_post_element = random.choice(ranged_element)
            actions = ActionChains(self.browser)
            time.sleep(random.random() + 0.5)
            actions.move_to_element(random_post_element)
            time.sleep(random.random() + 0.5)
            actions.click(on_element=random_post_element)
            time.sleep(random.random() + 0.5)
            actions.perform()
            time.sleep(random.random() + 1)
            print("어디까지 되는데?3")

            try:
                ui.WebDriverWait(self.browser, 15).until(EC.visibility_of_element_located((By.XPATH, "//time [contains(@class, '_aaqe')]/../..")))
                post_atag_btn = self.browser.find_element(By.XPATH, "//time [contains(@class, '_aaqe')]/../..")
                print("어디까지 되는데?4")
                time.sleep(random.random() + 0.5)
                post_atag_btn.click()
                print("어디까지 되는데?5")
            except:
                print("해시태그에서 포스트 선택하기를 실패했어요! 닫기를 실행합니다.")
                close_btn = self.browser.find_element(By.XPATH, "//*[local-name()='svg' and @aria-label='닫기']/../..")
                close_btn.click()
            time.sleep(random.random() + 2)
            return

        ui.WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div [contains(@class, '_aagw')]")))
        time.sleep(random.random() + 1)
        func_list = [scroll_down, choose_post]
        random.choice(func_list)()

        return
        

    @timer
    def get_where_am_i(self, current_url):
        if current_url == self.instagram_url:
            return 'main'
        elif "direct" in current_url:
            return 'dm'
        elif "explore" in current_url:
            return 'hashtag'
        return 'post'

# 메인, 게시글(post), dm, 해시태그채널, 비슷한계정, 팔로워, 팔로우, 탐험(나침반

# 메인
    # 스크롤 다운 (unrelated behavior)
    # 검색
    # 특정 포스트를 고르는 행위 (를 한다면, 고르기 이후는 이하의 포스트 기능사용)

# 메인 루틴
    # 1. 스크롤을 내린다(randomly)
    # 2. 내린 상태에서 selenium으로 parsing 가능한 article들을 불러온다.
    # 3. 보통 4~9개 정도의 article이 추출된다.
    # 4. article들 중 random article을 선택하여 post Routine을 실행한다.
    # 4-1. random 하게 좋아요를 누르고 다시 1로 넘어가거나
    # 4-2. 댓글 말풍선 버튼을 클릭하여 포스트 루틴을 시작한다.


# 포스트 (메인에서 포스트 보는 것도 동일하게 적용)
    # 포스트 채널 클릭 (채널로 이동)
    # 좋아요 - 하트버튼, 이미지 더블클릭
    # 이미지 넘기기 (여러장)
    # 이미지 1번 클릭 - 태그인물 pop
    # 댓글 풍선 - 포스트 popup (이미 포스트라면 댓글창 나옴), 댓글 x개 모두 보기도 동일
    # 게시 경과시간 - 해당 포스트를 팝업이 아닌곳에서 봄
    # 더보기 버튼 클릭
    # 각 버튼들 호버
    
    # 좋아요 xx개 버튼 - (위험) url은 같은데, 팝업이떠서 위험하다, 쓰지 않겠다.
    # 종이비행기 버튼 - DM 팝업, 여러모로 이상해서 안쓸기능
    # 대댓글 하트 - 안쓸기능
    # 포스트 저장 - 안쓸기능
    # 태그된 장소를 클릭 - 안쓸 기능(렉걸리고 인스타에서 거부하기도함)
    # 팔로우 (팔로잉) 클릭 - 안쓸 기능(메인에서는 안보여서 걍 안씀)

# 포스트 루틴
    # 1. 이미지가 여러개라면 옆으로 넘기기, 이미지 한번 클릭을 실행한다.
    # 2. 댓글을 scrolldown(up)한다.
    # 3. 좋아요를 누른다. (상태확인, 1번이상 금지)
    # 4. 댓글을 단다. (상태확인, 1번이상 금지)
    # 5. 팔로우를 한다. (상태확인, 1번이상 금지)
    # 6. xx명(좋아요 누른사람들) 을 클릭했다가 스크롤 몇번 내리고 나온다.
    # 7-1. 포스트를 남긴 채널로 이동한다.
    # 7-2. 새로운 루틴을 한다



# TODO: 
# 인스타그램 행위 - 해쉬태그검색, 좋아요, 댓글, 팔로워, 언팔로워, 팔로우, DM, id검색
# - 브라우저 행위로 이루어짐.
# - 행위를 여러가지로(될때까지):
# 1차 & 2차 행위로 나누고, Random 하게,
# 
# 행위, 횟수, 시간, ...., 
# 슬랙에 공유 회의 주제, 회의 내용, 회의 수준, 데드라인 - 슬랙 업무 공유 


    @timer
    def search(self, channel_id):
    # 검색창에 특정 채널 id 검색해서 해당 채널로 이동
        try:
            # search_input_form = self.browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[2]/input")
            search_input_form = self.browser.find_element(By.XPATH, "//input[contains(@placeholder, '검색')]")
            search_input_form.clear()
            time.sleep(random.random() + 1)
            search_input_form.send_keys(channel_id)
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "{channel_id} 인스타그램 채널을 검색합니다!".format(channel_id=channel_id))

            time.sleep(random.random() + 4)

            first_search_target_channel = ui.WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/{channel_id}/')]".format(channel_id=channel_id))))
            # first_search_target_channel = self.browser.find_element(By.XPATH, "//a[contains(@href,'/{channel_id}/')]".format(channel_id=channel_id))
            first_search_target_channel.click()
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "정상적으로 검색이 완료되었어요!")

            time.sleep(random.random() + 5)

            # #####django 저장
            # if InstagramChannel.objects.filter(channel_id=channel_id).exists() == False:
            #     channel_url = "https://www.instagram.com/{channel_id}/".format(channel_id=channel_id)
            #     # print(channel_url)
            #     channel_thumbnail = self.browser.find_element(By.XPATH, "//img [contains(@alt, '{channel_id}님의 프로필 사진')]".format(channel_id=channel_id)).get_attribute('src')
            #     # print(channel_thumbnail)
            #     InstagramChannel(channel_id=channel_id, channel_url=channel_url, channel_thumbnail=channel_thumbnail).save()


        except:
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "아이디 검색에 실패하여 url로 채널접속을 시도합니다.")
            self.browser.get(self.instagram_url + channel_id + "/")

        return


    # 메인에서 특정채널 검색해서 들어간다음에 메시지보내기 버튼 클릭
    @timer
    def activate_specific_channel_dm(self, channel_id):
        
        # 1. 특정채널 검색해서 들어가기
        self.search(channel_id)
        try:
            # 오류 페이지로 들어갔을 시 메인 페이지로 보냄
            self.browser.find_element(By.XPATH, "//h2 [contains(text(),'죄송합니다. 페이지를 사용할 수 없습니다.')]")
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "정상적인 채널에 입장하지 못하여 DM 보내기를 Pass합니다.")
            # print("정상적인 채널에 입장하지 못하여 DM 보내기를 Pass합니다.")
            return self.browser.get(self.instagram_url)
        except:
            pass
        

        # 2. 메시지 보내기 버튼 클릭
        check_if_succes = False
        try:
            send_message_button_element = ui.WebDriverWait(self.browser, 3).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'메시지 보내기')]/..")))
            send_message_button_element.click()
            check_if_succes = not check_if_succes
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "메시지 보내기 버튼 클릭에 성공했어요!")
        
        except:
            try:
                print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "메시지 보내기 버튼 클릭에 실패하여 follow요청 후 DM을 재시도 합니다!")
                # follow_button_element = self.browser.find_element(By.XPATH, "//h2[contains(text(), {channel_id})]/..//div[contains(text(), '팔로우')]".format(channel_id=channel_id))
                follow_button_element = self.browser.find_element(By.XPATH, "//div [text() = '팔로우']/..")
                follow_button_element.click()
                time.sleep(random.randrange(1,3) + 1)
                send_message_button_element = ui.WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'메시지 보내기')]/..")))
                send_message_button_element.click()
                time.sleep(random.randint(2,4) + 1)
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
            textarea_element = ui.WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, "//textarea[contains(@placeholder,'메시지 입력...')]")))
            textarea_element.clear()
            textarea_element.click()
            time.sleep(random.randrange(1,3) + 1)
            # self.browser.execute_script("arguments[0].value = arguments[1];", textarea_element , message)
            self.browser.execute_script("arguments[0].value=`" + message + "`;", textarea_element)
            textarea_element.send_keys(":D")
            time.sleep(random.randrange(1,2) + 1)
            textarea_element.send_keys(Keys.ENTER)
            time.sleep(random.randrange(1,3) + 1)
            
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "DM을 성공적으로 전송했습니다.")
            return True

        except:
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "DM 메시지 창에 도착했으나 DM보내기에 실패했어요!")
            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "랜딩 페이지로 돌아갑니다.")
            self.browser.get(self.instagram_url)
            self.browser.close()
            return False


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
        if self.get_current_url() != self.instagram_url:
            self.browser.get(self.instagram_url)
            time.sleep(random.randrange(1,3))

        time.sleep(random.random() + 1)
        is_valid_channel = self.activate_specific_channel_dm(channel_id)

        if is_valid_channel:
            return self.send_dm(message)

        return # None을 리턴한다. 


# 브라우징 행위 (클릭, 스크롤, 뒤로가기, 타이핑 ...)
a = {
    "collect_data": False or True,
    "url": "main" or "post" or "channel" or "dm" or "hashtag_channel" or "similar_accounts" or "follower" or "follow" or "explore",
    "is_searchable": False or True,
    "is_server_dead": False or True,
    "is_channel_private": True or False, # url: channel
    "is_commentable": True or False, # url: post
}