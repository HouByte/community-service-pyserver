# -*- coding: utf-8 -*-
# @Time : 2022/4/30 12:22
# @Author : Vincent Vic
# @File : UserController.py
# @Software: PyCharm
import json

import requests
from flask import Blueprint, request
from application import app
from common.lib.CommonResult import CommonResult
from config.wexin_setting import MINA_APP
from web.service.MemberService import MemberService

index_api = Blueprint('index_api', __name__)

'''
文档： https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html
获得临时登录凭证 GET https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code

'''
memberService = MemberService()

@index_api.post("/login")
def login():
    req = request.values;
    code = req['code'] if 'code' in req else ''
    if code is None or len(code) < 1:
        return CommonResult.failMsg("未提供授权code").toJson()
    nickName = req['nickName'] if 'nickName' in req else ''
    avatarUrl = req['avatarUrl'] if 'avatarUrl' in req else ''
    gender = req['gender'] if 'gender' in req else ''
    client_type = req['client_type'] if 'client_type' in req else 'wechat'
    info = memberService.login(code, nickName, avatarUrl, gender, client_type)
    return CommonResult.successData("登入成功", info)



