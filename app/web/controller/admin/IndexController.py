# -*- coding: utf-8 -*-
# @Time : 2022/4/30 13:21
# @Author : Vincent Vic
# @File : IndexController.py
# @Software: PyCharm
import json
import uuid

from flask import Blueprint, request, make_response, redirect, g

from application import app
from common.lib.Utils import ObjToJson
from common.lib.constant import ADMIN_TOKEN_KEY_REDIS, ADMIN_UID_KEY_REDIS
from common.lib.redis import Redis
from web.service.UserService import UserService
from common.lib.Response import Response
from common.lib.UrlManager import UrlManager
from common.lib.Helper import ops_render

page_index = Blueprint('index_page', __name__)

userService = UserService()


@page_index.route("/")
def index():
    return ops_render('index/index.html')


@page_index.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return ops_render('user/login.html')

    req = request.values;
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
    if login_name is None or len(login_name) < 4 or login_pwd is None or len(login_pwd) < 6:
        return Response.failMsg("登入失败【参数缺少或不符合规则】").toJson()
    data = {
        "login_name": login_name,
        "login_pwd": login_pwd
    }
    resp  = userService.login(data)
    if not resp:
        return resp.toJson()
    if not resp.isSuccess():
        return resp.toJson()
    cookieResponse = make_response(Response.successMsg("登入成功").toJson())

    user_info = resp.data
    token = str(uuid.uuid4())

    info = userService.getInfoJson(user_info)

    Redis.write(ADMIN_TOKEN_KEY_REDIS+token, json.dumps(info))
    Redis.write(ADMIN_UID_KEY_REDIS+str(user_info.uid), token)
    # cookie 存储token 1天
    cookieResponse.set_cookie(app.config['AUTH_COOKIE_NAME'], token, 60 * 60 * 24 * 1)

    return cookieResponse


@page_index.route("/logout")
def logout():
    response = make_response(redirect(UrlManager.buildUrl("/login")))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response
