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

PAGE_SIZE = 10
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    "1": "正常",
    "0": "冻结",
}

TYPE_MAPPING = {
    "0": "在找",
    "1": "提供",
}

NATURE_MAPPING = {
    "0": "互助",
    "1": "服务",
    "2": "公益",
}
