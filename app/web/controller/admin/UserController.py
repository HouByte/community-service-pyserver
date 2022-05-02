# -*- coding: utf-8 -*-
# @Time : 2022/4/30 12:22
# @Author : Vincent Vic
# @File : UserController.py
# @Software: PyCharm

from flask import Blueprint, request, g, make_response
from application import app
from common.lib.Helper import ops_render
from common.lib.Response import Response
from web.service.UserService import UserService

page_user = Blueprint('user_page', __name__)

userService = UserService()


@page_user.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == 'GET':
        return ops_render('user/edit.html')
    req = request.values;
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    if nickname is None or len(nickname) < 1 or email is None or len(email) < 1:
        return Response.failMsg("登入失败【参数缺少】").toJson()

    user_info = g.current_user
    user_info.nickname = nickname
    user_info.email = email
    user_info.mobile = mobile
    resp = userService.edit(user_info)
    return resp.toJson()


@page_user.route("/reset-pwd", methods=["GET", "POST"])
def resetPwd():
    if request.method == 'GET':
        return ops_render('user/reset_pwd.html')

    req = request.values;
    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''
    if old_password is None or len(old_password) < 1 or new_password is None or len(new_password) < 1:
        return Response.failMsg("登入失败【参数缺少】").toJson()

    user_info = g.current_user
    data = {
        "old_password": old_password,
        "new_password": new_password
    }
    resp = userService.resetPwd(user_info, data)
    if not resp:
        return resp.toJson()
    if not resp.isSuccess():
        return resp.toJson()
    response: any = make_response(resp.toJson())
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], resp.data)
    return response
