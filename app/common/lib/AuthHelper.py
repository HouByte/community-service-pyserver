# -*- coding: utf-8 -*-
# @Time : 2022/5/11 19:10
# @Author : Vincent Vic
# @File : AuthHelper.py
# @Software: PyCharm
from flask import render_template, g, request

from application import app
from common.lib.Helper import getCurrentDate
from common.lib.constant import API_TOKEN_KEY_REDIS, ADMIN_TOKEN_KEY_REDIS, ADMIN_LOG_UID_KEY_REDIS
from common.lib.redis import Redis
import json

def check_login():
    cookies = request.cookies
    token = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else None
    if token is None:
        return False

    try:
        info = Redis.read(ADMIN_TOKEN_KEY_REDIS + token)
        if not info:
            return False

        return json.loads(info)
    except Exception:
        return False


def get_member_login_id():
    """
    得到会员登入ID，如果未登入返回Flase
    """
    auth_Token = request.headers.get("Authorization")
    if auth_Token is None:
        return False
    info = Redis.read(API_TOKEN_KEY_REDIS + auth_Token)
    if not info:
        return False
    info = json.loads(info)
    return info['id'] if 'id' in info else False


def log(uid, url, args):
    currentDate = getCurrentDate()
    log = {
        'created_time': currentDate,
        'target_url': url,
        'args': args
    }
    Redis.hset(ADMIN_LOG_UID_KEY_REDIS + str(uid), currentDate, json.dumps(log))
    # 日志记录七天
    Redis.expire(ADMIN_LOG_UID_KEY_REDIS + str(uid), 60 * 60 * 24 * 7)
