import traceback
import requests
import re
import my_settings

class SeenamonDeco:

    def send_error_alarm(func):

        def send_line_alarm(text):
            url = 'https://api.line.me/v2/bot/message/push'
            headers = {
                'Content-type': 'application/json',
                'Authorization': 'Bearer {fXdYl0WN73iUGMAMK1SQ2puv75KGmdsjUHgQlRXK+epEzaT3sXsJaz/co7KklzuMUKe+BedJA0gNzSeXCs3cqMCZW0r0MG7jVdOgm9OyVYOvLCJQKa7/QG3t3llZsoAQXWd42oVpe73MovBsGyQjAAdB04t89/1O/w1cDnyilFU=}',
                }
            line_user_id = my_settings.line_id
            data = {
                "to": line_user_id,
                "messages":[
                    {
                        "type": "text",
                        "text": f"{text}",
                        
                        }
                    ],
                }
            # requests.post(url=url, json=data, headers=headers)

        def wrapper(*args, **kwargs):
            context = {}
            context['func_name'] = func.__name__
            try:
                func_return = func(*args, **kwargs)
                return func_return
            except Exception as e:
                context['error'] = traceback.format_exc()
                send_line_alarm(str(context))
            
        return wrapper


class Test:
    def __init__(self) -> None:
        self.a = 1

    @SeenamonDeco.send_error_alarm
    def abc(self):
        a = "fs" + 1
        print(self.a)

a = Test().abc()








