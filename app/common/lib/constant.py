# -*- coding: utf-8 -*-
# @Time : 2022/5/2 19:44
# @Author : Vincent Vic
# @File : constant.py
# @Software: PyCharm

ADMIN_TOKEN_KEY_REDIS = 'ADMIN_TOKEN_KEY_REDIS_'
ADMIN_UID_KEY_REDIS = 'ADMIN_UID_KEY_REDIS_'
ADMIN_LOG_UID_KEY_REDIS = 'ADMIN_LOG_UID_KEY_REDIS_'

API_TOKEN_KEY_REDIS = 'API_TOKEN_KEY_REDIS_'
API_UID_KEY_REDIS = 'API_UID_KEY_REDIS_'


class ServiceStatus:
    # 待发布
    UNPUBLISHED = 0
    # 待审核
    PENDING = 1
    # 已发布
    PUBLISHED = 2
    # 已下架
    OFF_SHELVES = 3
    # 审核不通过
    DENY = 4


class OrderStatus:
    UNAPPROVED = 0
    UNPAID = 1
    UNCONFIRMED = 2
    UNRATED = 3
    COMPLETED = 4
    CANCELED = 5
    REFUSED = 6
