# -*- coding: utf-8 -*-
# @Time : 2022/4/30 8:57
# @Author : Vincent Vic
# @File : base_setting.py
# @Software: PyCharm
AUTH_COOKIE_NAME = 'COMMUNITY_PYS'

# 过滤 url
IGNORE_URLS = [
    "^/login"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

API_IGNORE_URLS = [
    "^/api"
]

PAGE_SIZE = 50
PAGE_DISPLAY = 10

MINA_APP = {
    "appid": "wx759d38ee4da2062d",
    "appkey": "fd6661994ed89a5d79d8d6f6999d2931",
    "paykey": "xxxxxxxxxxxxxx换自己的",
    "mch_id": "xxxxxxxxxxxx换自己的",
    "callback_url": "/api/order/callback"
}
