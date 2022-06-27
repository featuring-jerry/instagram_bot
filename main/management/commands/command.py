from django.core.management.base import BaseCommand, CommandError
import my_settings
from main.instagram_crawler import InstagramBot

class Command(BaseCommand):
    help = 'Closes the specified channel Id for crawler'

    def add_arguments(self, parser):
        parser.add_argument('channel_id', type=str)
        
    def handle(self, *args, **options):
        channel_id = options['channel_id']
        # try:
        #     target_channel = InstagramChannel.objects.get(channel_id=channel_id)
        # except InstagramChannel.DoesNotExist:
        #     raise CommandError("Channel Id '%s' does not exist" % channel_id)
        
        try:
            insta_bot = InstagramBot(my_settings.user_id, my_settings.user_passwd)
            insta_bot.log_in()
            insta_bot.set_permisson()
            self.stdout.write(self.style.SUCCESS("성공적으로 로그인, '%s' 채널을 검색합니다." % channel_id))
        except:
            raise CommandError(" '%s' 채널이 존재하지 않습니다 " % channel_id)
        
        try:
            insta_bot.direct_message(channel_id, "Hey moons, this is Jerry's msg by Instagram_bot dev_2 version!")
            self.stdout.write(self.style.SUCCESS("성공적으로 '%s' 채널에게 DM을 보냈습니다." % channel_id))
        except:
            raise CommandError(" '%s' 에게 DM 전송이 실패했어요" % channel_id)

        insta_bot.opened = False

        # target_channel.save()

        self.stdout.write(self.style.SUCCESS("성공적으로 임무를 완수하고 '%s'을 종료합니다." % channel_id))