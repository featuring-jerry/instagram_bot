from django.db import models

# Create your models here.

class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['created_at']

# class Etag(CommonInfo):
#     etag = models.CharField(max_length=50, blank=True, null=True)

#     class Meta:
#         abstract = True
#         ordering = ['etag']

class InstagramChannel(CommonInfo):
    channel_id = models.CharField(max_length=50, unique=True)
    channel_url = models.CharField(max_length=100)
    channel_thumbnail = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.channel_id + "의 인스타 채널"

class ChannelStatistics(CommonInfo):
    target_channel = models.OneToOneField("InstagramChannel", related_name="channelstatistics", on_delete=models.CASCADE)
    post_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)
    follow_count = models.IntegerField(default=0)

    def __str__(self):
        return self.target_channel.InstagramChannel.channel_id + "인스타 채널의 통계자료"

class ChannelPost(CommonInfo):
    target_channel = models.ForeignKey("InstagramChannel", related_name="channelpost", on_delete=models.CASCADE)

    post_id = models.CharField(max_length=50, unique=True)
    post_url = models.CharField(max_length=100)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    post_thumbnail = models.CharField(max_length=100, blank=True, null=True)

    published_at = models.DateTimeField(verbose_name="Date Published")

    def __str__(self):
        return self.target_channel.InstagramChannel.channel_id + "인스타 채널의" + self.post_id + "포스트 내용"