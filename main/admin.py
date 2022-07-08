from django.contrib import admin
from main.models import DMChecker, InstagramChannel,ChannelStatistics,ChannelPost,DirectMessage,DMChecker
# Register your models here.

admin.site.register(InstagramChannel)
admin.site.register(ChannelStatistics)
admin.site.register(ChannelPost)
admin.site.register(DirectMessage)
admin.site.register(DMChecker)