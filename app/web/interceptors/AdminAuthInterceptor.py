# -*- coding: utf-8 -*-
# @Time : 2022/4/30 21:33
# @Author : Vincent Vic
# @File : AdminAuthInterceptor.py
# @Software: PyCharm
import json
import re

from flask import request, redirect, g

from application import app
from common.lib.Helper import getCurrentDate
from common.lib.UrlManager import UrlManager
from common.lib.constant import ADMIN_TOKEN_KEY_REDIS, ADMIN_LOG_UID_KEY_REDIS
from common.lib.redis import Redis
from web.service.UserService import UserService

userService = UserService()


@app.before_request
def before_request():
    ignore_urls = app.config["IGNORE_URLS"]
    ignore__check_login_urls = app.config["IGNORE_CHECK_LOGIN_URLS"]
    path = request.path

    pattern = re.compile("%s" % "|".join(ignore__check_login_urls))
    if pattern.match(path):
        return

    if "/api" in path:
        return


    user_info = check_login()

    g.current_user = None
    if user_info:
        g.current_user = user_info
    pattern = re.compile("%s" % "|".join(ignore_urls))
    if pattern.match(path):
        return

    if not user_info:
        return redirect(UrlManager.buildUrl('/login'))

    log(user_info['uid'], path, request.args)
    return


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


def log(uid, url, args):
    currentDate = getCurrentDate()
    log = {
        'created_time': currentDate,
        'target_url': url,
        'args': args
    }
    Redis.hset(ADMIN_LOG_UID_KEY_REDIS+str(uid), currentDate, json.dumps(log))
    # 日志记录七天
    Redis.expire(ADMIN_LOG_UID_KEY_REDIS+str(uid), 60*60*24*7)

