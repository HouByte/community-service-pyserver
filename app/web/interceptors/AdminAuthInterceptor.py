# -*- coding: utf-8 -*-
# @Time : 2022/4/30 21:33
# @Author : Vincent Vic
# @File : AdminAuthInterceptor.py
# @Software: PyCharm
import json
import re

from flask import request, redirect, g
from application import app
from common.lib.constant import ADMIN_TOKEN_KEY_REDIS
from common.lib.redis import Redis
from web.model.User import User
from web.service.UserService import UserService
from common.lib.UrlManager import UrlManager

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
    return


def check_login():
    cookies = request.cookies
    token = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else None
    if token is None:
        return False
    # auth_info = auth_cookies.split("#")
    # if len(auth_info) != 2:
    #     return False

    try:
        # user_info = User.query.filter_by(uid=auth_info[1]).first()
        # if user_info is None:
        #     return False
        # if auth_info[0] != userService.geneAuthCode(user_info):
        #     return False
        # return user_info
        info = Redis.read(ADMIN_TOKEN_KEY_REDIS+token)
        if not info:
            return False

        return json.loads(info)
    except Exception:
        return False
