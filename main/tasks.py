# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from main import instagram_crawler

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

# @shared_task
# def send_dm(channel_id, msg):

