from telnetlib import DM
from django.core.management.base import BaseCommand, CommandError
import my_settings
from main.instagram_crawler import InstagramBot, InstagramHangoutBot
import time
from main.models import DMChecker, DirectMessage
from datetime import datetime, timezone, timedelta

class Command(BaseCommand):
    help = 'Closes the specified channel Id for crawler'
    life_count = 30

    def add_arguments(self, parser):
        # parser.add_argument('channel_id', type=str)
        parser.add_argument('random_count', type=int)
        
    def handle(self, *args, **options):
        # channel_id = options['channel_id']
        random_count = options['random_count']
        start = True
        # try:
        #     target_channel = InstagramChannel.objects.get(channel_id=channel_id)
        # except InstagramChannel.DoesNotExist:
        #     raise CommandError("Channel Id '%s' does not exist" % channel_id)
        while self.life_count != 0:
            try:
                # hangout_bot = InstagramHangoutBot(my_settings.user_id, my_settings.user_passwd, "facebook")
                # hangout_bot = InstagramHangoutBot(my_settings.instagram_id, my_settings.instagram_pw, "instagram")
                hangout_bot = InstagramHangoutBot(my_settings.instagram_test_id, my_settings.instagram_test_pw, "instagram")
                hangout_bot.log_in()
                hangout_bot.set_permisson()
                self.stdout.write(self.style.SUCCESS("성공적으로 로그인했습니다."))
                if not start:
                    hangout_bot.random_activity()
                # count = 1
                
                timestamp = False
                dm_interval = 5
                while True:
                    # if count > 100:
                    if random_count == 0:
                        break
                    if not timestamp:
                        dm_interval_decider = int(str(datetime.now(timezone(timedelta(hours=9))).time())[:2])
                        if dm_interval_decider >= 8 and dm_interval_decider < 18:
                            dm_interval = 5
                        elif dm_interval_decider >= 18:
                            dm_interval = 6
                        else:
                            dm_interval = 5
                            while True:
                                dm_interval_decider = int(str(datetime.now(timezone(timedelta(hours=9))).time())[:2])
                                if dm_interval_decider < 8: # 8시까지 5분씩 수면
                                    print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "오전 8시가 될 때까지 10분씩 계속 잠자요~")
                                    time.sleep(600)
                                else:
                                    break
                            # time.sleep(30000) # 9시간 수면
                            

                        print(dm_interval, "분 간격으로 DM을 보냅니다.")

                        if DirectMessage.objects.filter().exists() == True:
                            
                            
                            target_channel = DirectMessage.objects.filter()[0]
                            target_channel_id = target_channel.target_channel_id
                            # DMChecker.objects.update_or_create(channel_id=target_channel, defaults={'is_dm_sent': True})
                            if DMChecker.objects.filter(channel_id=target_channel_id).exists() == False:
                                DMChecker.objects.create(channel_id=target_channel_id)
                                
                                message = target_channel.message
                                target_channel.delete()
                                
                                try: 
                                    hangout_bot.direct_message(target_channel_id, message)
                                    obj = DMChecker.objects.get(channel_id=target_channel_id)
                                    obj.is_dm_sent = True
                                    obj.save()
                                    self.stdout.write(self.style.SUCCESS("성공적으로 '%s' 채널에게 DM을 보냈습니다." % target_channel_id))
                                    timestamp = int(str(datetime.now(timezone(timedelta(hours=9))).time())[:2]) * 60 + int(str(datetime.now(timezone(timedelta(hours=9))).time())[3:5])

                                except:
                                    raise CommandError(" '%s' 에게 DM 전송이 실패했어요" % target_channel_id)
                            else:
                                if DMChecker.objects.get(channel_id=target_channel_id).is_dm_sent == False:
                                    message = target_channel.message
                                    target_channel.delete()

                                    try: 
                                        check_result = hangout_bot.direct_message(target_channel_id, message)
                                        if check_result:
                                            obj = DMChecker.objects.get(channel_id=target_channel_id)
                                            obj.is_dm_sent = True ## 
                                            obj.save()
                                            self.stdout.write(self.style.SUCCESS("성공적으로 '%s' 채널에게 DM을 보냈습니다." % target_channel_id))
                                            timestamp = int(str(datetime.now(timezone(timedelta(hours=9))).time())[:2]) * 60 + int(str(datetime.now(timezone(timedelta(hours=9))).time())[3:5])
                                        elif check_result == False:
                                            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "일시정지일 가능성이 높습니다, life count와 random_count를 줄여 프로그램을 종료하도록 하겠습니다.")
                                            random_count = 0
                                            self.life_count = 0
                                        else: # None 결과값이 Return 되었을 때
                                            print(str(datetime.now(timezone(timedelta(hours=9))).time())[:8], "존재하지 않는 채널일 가능성이 있습니다. '%s'채널이 유효한 아이디인지 확인하세요." % target_channel_id)

                                    except:
                                        raise CommandError(" '%s' 에게 DM 전송이 실패했어요" % target_channel_id)
                                else:
                                    target_channel.delete()
                                    time.sleep(3)
                            
                    else:
                        now = int(str(datetime.now(timezone(timedelta(hours=9))).time())[:2]) * 60 + int(str(datetime.now(timezone(timedelta(hours=9))).time())[3:5])
                        if now - timestamp >= dm_interval:
                            timestamp = False
                    random_count -= 1
                    hangout_bot.random_activity()               

                time.sleep(5)
                # count = count + 1



                # insta_bot = InstagramBot(my_settings.user_id, my_settings.user_passwd)
                # insta_bot.log_in()
                # insta_bot.set_permisson()
                # self.stdout.write(self.style.SUCCESS("성공적으로 로그인했습니다."))
                # insta_bot.random_hashtag_play([2],3,3)
                # self.stdout.write(self.style.SUCCESS("'%s' 채널을 검색합니다." % channel_id))
            except:
                if self.life_count == 0:
                    raise CommandError("인스타 봇이 출동을 실패했어요")
                else:
                    start = False
                    self.life_count -= 1
                    hangout_bot.browser.close()
                    time.sleep(5)

        
        # try:
        #     insta_bot.direct_message(channel_id, "Hey moons, this is Jerry's msg by Instagram_bot dev_2 version!")
        #     self.stdout.write(self.style.SUCCESS("성공적으로 '%s' 채널에게 DM을 보냈습니다." % channel_id))
        # except:
        #     raise CommandError(" '%s' 에게 DM 전송이 실패했어요" % channel_id)

        # insta_bot.opened = False

        # target_channel.save()

        # self.stdout.write(self.style.SUCCESS("성공적으로 임무를 완수하고 '%s'을 종료합니다." % channel_id))
        self.stdout.write(self.style.SUCCESS("성공적으로 임무를 완수하고 'insta_bot'을 종료합니다."))