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
    url = 'https://v0.yiketianqi.com/api?unescape=1&version=v62&appid=36449493&appsecret=TWylYl3Y&cityid=101060101'
    res = requests.get(url)
    res = res.json()
    return res['wea'],res['tem'],res['tem1'],res['tem2'],res['air_tips'],res['air_level'],res['zhishu']['chuanyi']['tips']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  t = date.today()
  next = datetime.strptime(str(t.year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
    t = next - today
  return t.days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature,temperature1, temperature2,tips,level,tip2 = get_weather()
data = {"weather":{"value":wea, "color":get_random_color()},"temperature":{"value":temperature},"temperature1":{"value":temperature1},"temperature2":{"value":temperature2},"level":{"value":level},"tips":{"value":tips},"tip2":{"value":tip2},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
res = wm.send_template("ok5zp6T4LmcwUUzl5DnAJaE_zYOM", template_id, data)
print(res)
