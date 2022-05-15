# -*- coding: utf-8 -*-
# @Time : 2022/4/30 13:21
# @Author : Vincent Vic
# @File : IndexController.py
# @Software: PyCharm
import json
import uuid

from flask import Blueprint, request, make_response, redirect

from application import app
from common.lib.CommonResult import CommonResult
from common.lib.Helper import ops_render
from common.lib.UrlManager import UrlManager
from common.lib.constant import ADMIN_TOKEN_KEY_REDIS, ADMIN_UID_KEY_REDIS
from common.lib.redis import Redis
from web.service.MemberService import MemberService
from web.service.OrderService import OrderService
from web.service.SService import SService
from web.service.UserService import UserService

page_index = Blueprint('index_page', __name__)

userService = UserService()
orderService = OrderService()
sService = SService()
memberService = MemberService()


@page_index.route("/")
def index():
    orderService.getVolume()
    resp_data = {

        'order': orderService.getVolume(),
        'service': sService.getVolume(),
        'member': memberService.getVolume()
    }
    return ops_render('index/index.html', resp_data)


@page_index.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return ops_render('user/login.html')

    req = request.values;
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
    if login_name is None or len(login_name) < 4 or login_pwd is None or len(login_pwd) < 6:
        return CommonResult.failMsg("登入失败【参数缺少或不符合规则】")
    data = {
        "login_name": login_name,
        "login_pwd": login_pwd
    }
    user_info = userService.login(data)
    cookieResponse = make_response(CommonResult.successMsg("登入成功"))
    # token 记录
    token = str(uuid.uuid4())
    info = userService.getInfoJson(user_info)
    Redis.write(ADMIN_TOKEN_KEY_REDIS + token, json.dumps(info))
    Redis.write(ADMIN_UID_KEY_REDIS + str(user_info.uid), token)
    # cookie 存储token 1天
    cookieResponse.set_cookie(app.config['AUTH_COOKIE_NAME'], token, 60 * 60 * 24 * 1)

    return cookieResponse


@page_index.route("/logout")
def logout():
    response = make_response(redirect(UrlManager.buildUrl("/login")))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response
