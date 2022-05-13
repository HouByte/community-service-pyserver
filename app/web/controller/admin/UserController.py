# -*- coding: utf-8 -*-
# @Time : 2022/4/30 12:22
# @Author : Vincent Vic
# @File : UserController.py
# @Software: PyCharm
import json

from flask import Blueprint, request, g, redirect

from common.lib.APIException import APIParameterException
from common.lib.CommonResult import CommonResult
from common.lib.Helper import ops_render
from common.lib.UrlManager import UrlManager
from common.lib.Utils import isEmail, isMobile, isPwd
from common.lib.constant import ADMIN_TOKEN_KEY_REDIS, ADMIN_UID_KEY_REDIS
from common.lib.redis import Redis
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
    sex = req['sex'] if 'sex' in req else ''

    if nickname is None or len(nickname) < 1:
        raise APIParameterException("请输入符合规范的姓名")
    if not isMobile(mobile):
        raise APIParameterException("请输入符合规范的手机号码")
    if not isEmail(email):
        raise APIParameterException("请输入符合规范的邮箱")

    user_info = userService.getUser(g.current_user['uid'])
    if not user_info:
        raise APIParameterException("用户不存在")
    user_info.nickname = nickname
    user_info.email = email
    user_info.mobile = mobile
    user_info.sex = sex

    userService.edit(user_info)

    # redis 更新数据
    info = userService.getInfoJson(user_info)
    token = Redis.read(ADMIN_UID_KEY_REDIS + str(user_info.uid))
    if not token:
        return redirect(UrlManager.buildUrl('/login'))
    Redis.write(ADMIN_TOKEN_KEY_REDIS + token, json.dumps(info))

    return CommonResult.successMsg("更新成功")


@page_user.route("/reset-pwd", methods=["GET", "POST"])
def resetPwd():
    if request.method == 'GET':
        return ops_render('user/reset_pwd.html')

    req = request.values;
    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''
    if old_password is None or len(old_password) < 1 or not isPwd(new_password):
        raise APIParameterException("修改失败【参数缺少或密码太弱】")

    user_info = g.current_user
    data = {
        "old_password": old_password,
        "new_password": new_password
    }
    userService.resetPwd(user_info, data)
    return CommonResult.successMsg("更新成功")
