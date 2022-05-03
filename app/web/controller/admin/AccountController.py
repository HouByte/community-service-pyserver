# -*- coding: utf-8 -*-
# @Time : 2022/4/30 14:08
# @Author : Vincent Vic
# @File : AccountController.py
# @Software: PyCharm
import json

from flask import Blueprint, request, redirect, g
from common.lib.Helper import ops_render
from common.lib.Response import Response
from common.lib.UrlManager import UrlManager
from common.lib.Utils import isMobile, isEmail, isPwd, isUsername
from common.lib.constant import ADMIN_UID_KEY_REDIS, ADMIN_TOKEN_KEY_REDIS, ADMIN_LOG_UID_KEY_REDIS
from common.lib.redis import Redis
from web.service.UserService import UserService
from application import app

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
            log = {
                'created_time': item[0].decode(),
                'target_url': item[1].decode()
            }
            access_list.append(log)
    print(access_list)
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
        return Response.failMsg("请输入符合规范的姓名").toJson()
    if not isMobile(mobile):
        return Response.failMsg("请输入符合规范的手机号码").toJson()
    if not isEmail(email):
        return Response.failMsg("请输入符合规范的邮箱").toJson()
    if not isUsername(login_name):
        return Response.failMsg("请输入符合规范的登录用户名").toJson()
    # 新增的情况下： 密码能为空，或不能小于6
    if uid < 1 and not isPwd(login_pwd):
        return Response.failMsg("请输入登录密码太弱了，不被允许").toJson()
    # 修改的情况下且密码不为空且小于6，不被允许
    if uid > 1 and login_pwd.strip() != '' and not isPwd(login_pwd):
        return Response.failMsg("请输入登录密码太弱了，不被允许").toJson()

    data = {
        'nickname': nickname,
        'email': email,
        'mobile': mobile,
        'login_name': login_name,
        'login_pwd': login_pwd,
        'sex': sex,
        'uid': uid
    }
    resp = userService.set(data)
    # redis 更新数据
    info = userService.getInfoJson(resp.data)
    token = Redis.read(ADMIN_UID_KEY_REDIS + str(info['uid']))
    if token is not None:
        Redis.write(ADMIN_TOKEN_KEY_REDIS + token, json.dumps(info))
    return resp.toSimpleJson()


@page_account.route("/ops", methods=["POST"])
def ops():
    req = request.values
    act = req['act'] if 'act' in req else None
    id = req['id'] if 'id' in req else None
    if not act or not id:
        return Response.failMsg("参数错误")
    if int(id) == 1:
        return Response.failMsg("超级管理员不允许被操作")
    if g.current_user['login_name'] != 'root':
        return Response.failMsg("账户操作只允许超级管理员操作")
    data = {
        'act': act,
        'id': id
    }
    resp = userService.ops(data)
    if act == 'remove':
        # redis 更新数据
        info = userService.getInfoJson(resp.data)
        token = Redis.read(ADMIN_UID_KEY_REDIS + str(info['uid']))
        if token is not None:
            Redis.write(ADMIN_TOKEN_KEY_REDIS + token, json.dumps(info))
    return resp.toSimpleJson()
