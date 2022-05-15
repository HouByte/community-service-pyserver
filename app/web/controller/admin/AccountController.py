# -*- coding: utf-8 -*-
# @Time : 2022/4/30 14:08
# @Author : Vincent Vic
# @File : AccountController.py
# @Software: PyCharm
import json

from flask import Blueprint, request, redirect, g

from application import app
from common.lib.APIException import APIParameterException
from common.lib.CommonResult import CommonResult
from common.lib.Helper import ops_render, getOpsData
from common.lib.UrlManager import UrlManager
from common.lib.Utils import isMobile, isEmail, isPwd, isUsername
from common.lib.constant import ADMIN_UID_KEY_REDIS, ADMIN_TOKEN_KEY_REDIS, ADMIN_LOG_UID_KEY_REDIS
from common.lib.redis import Redis
from web.service.UserService import UserService

page_account = Blueprint('account_page', __name__)

userService = UserService()


@page_account.route("/index")
def index():
    req = request.args
    page_params = {
        'total': 0,
        'page_size': app.config['PAGE_SIZE'],
        'page': int(req.get('page', 1)),
        'display': app.config['PAGE_DISPLAY'],
        'mix_kw': req.get('mix_kw', ''),
        'status': req.get('status', -1)
    }

    resp_data = userService.getUserList(page_params)
    resp_data["status_mapping"] = app.config["STATUS_MAPPING"]
    resp_data["search_con"] = req
    return ops_render('account/index.html', resp_data)


def getUserInfo():
    req = request.args
    uid = int(req.get('id', 0))
    reback_url = UrlManager.buildUrl("/account/index")
    if uid < 1:
        return redirect(reback_url)
    info = userService.getUserInfo(uid)
    if not info:
        return redirect(reback_url)
    resp_data = {
        'user_info': info
    }
    return resp_data


@page_account.route("/info")
def info():
    resp_data = getUserInfo()
    logs = Redis.hgetall(ADMIN_LOG_UID_KEY_REDIS + str(resp_data['user_info'].uid))
    access_list = []
    print(logs)
    if logs:
        for item in logs.items():
            log = json.loads(item[1].decode())
            access_list.append(log)
    resp_data['access_list'] = access_list
    return ops_render('account/info.html', resp_data)


@page_account.route("/set", methods=["GET", "POST"])
def set():
    if request.method == 'GET':
        req = request.args
        uid = int(req.get('id', 0))
        if uid > 0:
            info = userService.getUserInfo(uid)
        if uid < 1 or not info:
            info = {
                'nickname': '',
                'mobile': '',
                'email': '',
                'avatar': '',
                'login_name': '',
                'login_pwd': '',
                'sex': 0
            }
        resp_data = {
            "user_info": info
        }
        return ops_render('account/set.html', resp_data)
    req = request.values;
    uid = int(req['id'] if 'id' in req else -1)
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
    sex = req['sex'] if 'sex' in req else 0

    if nickname is None or len(nickname) < 1:
        raise APIParameterException("请输入符合规范的姓名")
    if not isMobile(mobile):
        raise APIParameterException("请输入符合规范的手机号码")
    if not isEmail(email):
        raise APIParameterException("请输入符合规范的邮箱")
    if not isUsername(login_name):
        raise APIParameterException("请输入符合规范的登录用户名")
    # 新增的情况下： 密码能为空，或不能小于6
    if uid < 1 and not isPwd(login_pwd):
        raise APIParameterException("请输入登录密码太弱了，不被允许")
    # 修改的情况下且密码不为空且小于6，不被允许
    if uid > 1 and login_pwd.strip() != '' and not isPwd(login_pwd):
        raise APIParameterException("请输入登录密码太弱了，不被允许")

    data = {
        'nickname': nickname,
        'email': email,
        'mobile': mobile,
        'login_name': login_name,
        'login_pwd': login_pwd,
        'sex': sex,
        'uid': uid
    }
    model_user = userService.set(data)
    # redis 更新数据
    info = userService.getInfoJson(model_user)
    token = Redis.read(ADMIN_UID_KEY_REDIS + str(info['uid']))
    if token is not None:
        Redis.write(ADMIN_TOKEN_KEY_REDIS + token, json.dumps(info))
    return CommonResult.successMsg("更新成功")


@page_account.route("/ops", methods=["POST"])
def ops():
    data = getOpsData(request.values)
    if int(data['id']) == 1:
        raise APIParameterException("超级管理员不允许被操作")
    if g.current_user['login_name'] != 'root':
        raise APIParameterException("账户操作只允许超级管理员操作")
    user_info = userService.ops(data)
    # redis 更新数据
    info = userService.getInfoJson(user_info)
    token = Redis.read(ADMIN_UID_KEY_REDIS + str(info['uid']))
    if data['act'] == 'remove':
        Redis.delete(ADMIN_TOKEN_KEY_REDIS + token)
    elif token is not None:
        Redis.write(ADMIN_TOKEN_KEY_REDIS + token, json.dumps(info))
    return CommonResult.successMsg("更新成功")
