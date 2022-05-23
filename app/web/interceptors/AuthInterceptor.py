# -*- coding: utf-8 -*-
# @Time : 2022/4/30 21:33
# @Author : Vincent Vic
# @File : AuthInterceptor.py
# @Software: PyCharm
import re

from flask import request, redirect, g

from application import app
from common.lib.AuthHelper import get_member_login_id, check_login, log
from common.lib.UrlManager import UrlManager
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


@app.before_request
def api_before():
    path = request.path
    if "/api" not in path:
        return
    id = get_member_login_id()


    return
