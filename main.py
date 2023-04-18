from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
# start_date='2022-02-02'  # 可将上面的start_date进行注释，将本行的注释取消，填入相对应的日期即可。
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
# birthday='01-01'  # 可将上面的birthday进行注释，将本行的注释取消，填入相对应的日期即可。
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

def get_weather():
    url = "http://www.weather.com.cn/data/cityinfo/101060101.html"
    r = requests.get(url)
    res=r.json()
    weather = res['weatherinfo']
    return weather['weather'], weather['temp1'], weather['temp2']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
url = "http://www.weather.com.cn/data/cityinfo/101060101.html"
r = requests.get(url,headers=headers)
print("开始")
print(r)
print('结束')
wea, temperature1, temperature2 = '暂时有问题','暂时有问题','暂时有问题'
data = {"weather":{"value":wea},"temperature1":{"value":temperature1},"temperature2":{"value":temperature2},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
