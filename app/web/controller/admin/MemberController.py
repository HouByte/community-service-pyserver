# -*- coding: utf-8 -*-
# @Time : 2022/4/30 14:13
# @Author : Vincent Vic
# @File : MemberController.py
# @Software: PyCharm
from flask import Blueprint, request

from application import app
from common.lib.APIException import APIParameterException
from common.lib.CommonResult import CommonResult
from common.lib.Helper import ops_render, getOpsData, getPageParams
from common.lib.constant import API_UID_KEY_REDIS, API_TOKEN_KEY_REDIS
from common.lib.redis import Redis
from web.service.MemberService import MemberService

page_member = Blueprint('member_page', __name__)
memberService = MemberService()

@page_member.route("/index")
def index():
    req = request.args
    page_params = getPageParams(req, app)
    resp_data = memberService.getMemberList(page_params)
    resp_data["status_mapping"] = app.config["STATUS_MAPPING"]
    resp_data["search_con"] = req
    return ops_render('member/index.html', resp_data)

@page_member.route("/ops", methods=["POST"])
def ops():
    data = getOpsData(request.values)

    id = memberService.ops(data)
    token = Redis.read(API_UID_KEY_REDIS + str(id))
    if token:
        Redis.delete(API_TOKEN_KEY_REDIS + token)
        Redis.delete(API_UID_KEY_REDIS + str(id))

    return CommonResult.successMsg("操作成功")
