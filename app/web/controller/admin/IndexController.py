# -*- coding: utf-8 -*-
# @Time : 2022/4/30 13:21
# @Author : Vincent Vic
# @File : IndexController.py
# @Software: PyCharm
import json

from flask import Blueprint, request, make_response, redirect, g

from application import app
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
    if login_name is None or len(login_name) < 1 or login_pwd is None or len(login_pwd) < 1:
        return Response.failMsg("登入失败【参数缺少】").toJson()
    data = {
        "login_name": login_name,
        "login_pwd": login_pwd
    }
    resp = userService.login(data)
    if not resp:
        return resp.toJson()
    if not resp.isSuccess():
        return resp.toJson()
    response: any = make_response(resp.toJson())
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], resp.data)
    return response


@page_index.route("/logout")
def logout():
    response = make_response(redirect(UrlManager.buildUrl("/login")))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response
