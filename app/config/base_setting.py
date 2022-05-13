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

SERVICE_STATUS_MAPPING = {
    "0": "待发布",
    "1": "待审核",
    "2": "已发布",
    "3": "已下架",
    "4": "已取消",
    "5": "审核不通过"
}

ORDER_STATUS_MAPPING = {
    "0": "未同意",
    "1": "未支付",
    "2": "未确认",
    "3": "未评价",
    "4": "完成",
    "5": "取消",
    "6": "拒绝"
}

TYPE_MAPPING = {
    "1": "提供",
    "2": "在找",

}

NATURE_MAPPING = {
    "0": "互助",
    "1": "服务",
    "2": "公益",
}
