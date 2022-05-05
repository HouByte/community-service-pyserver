# -*- coding: utf-8 -*-
# @Time : 2022/4/30 14:13
# @Author : Vincent Vic
# @File : MemberController.py
# @Software: PyCharm
from flask import Blueprint, request

from application import app
from common.lib.Helper import ops_render, getOpsData, getPageParams
from common.lib.Response import Response
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
    if not data['act'] or not data['id']:
        return Response.failMsg("参数错误")

    resp = memberService.ops(data)
    if resp.success():
        # redis 更新数据
        id = resp.data
        token = Redis.read(API_UID_KEY_REDIS + str(id))
        if token:
            Redis.delete(API_TOKEN_KEY_REDIS + token)
            Redis.delete(API_UID_KEY_REDIS + str(id))

    return resp.toSimpleJson()
