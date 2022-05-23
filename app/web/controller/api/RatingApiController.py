# -*- coding: utf-8 -*-
# @Time : 2022/4/30 12:22
# @Author : Vincent Vic
# @File : UserController.py
# @Software: PyCharm
from flask import Blueprint, request

from application import app
from common.lib.APIException import APIParameterException, APIAuthFailed
from common.lib.AuthHelper import get_member_login_id
from common.lib.CommonResult import CommonResult
from common.lib.Helper import getPageParams
from web.service.OrderService import OrderService
from web.service.RatingService import RatingService

rating_api = Blueprint('rating_api', __name__)

ratingService = RatingService()

orderService = OrderService()

# {
#     "id": 0,
#     "score": 0,
#     "content": "",
#     "illustration": [],
#     "created": '',
#     "author": {
#         "nickname": "",
#         "avatarUrl": ""
#     }
# }


@rating_api.get("/list")
def list():
    req = request.args
    sid = int(req.get("sid", -1))
    if sid < 0:
        raise APIParameterException("id异常")
    page_params = getPageParams(req, app)
    page_params['sid'] = sid
    resp_data = ratingService.getRatingList(page_params)
    pages = resp_data['pages']
    resp_data['pages'] = {
        'page_size': pages['page_size'],
        'total': pages['total'],
        'is_next': pages['is_next']
    }
    list = []
    rating_list = resp_data['list']

    for rating in rating_list:
        item = ratingService.toVo(rating)
        list.append(item)
    resp_data['list'] = list

    return CommonResult.successDictData("list", resp_data)

@rating_api.get("/order")
def getRatingByOrder():
    req = request.args
    oid = int(req.get("oid", -1))
    if oid < 0:
        raise APIParameterException("id异常")
    resp_data = ratingService.getRatingByOrder(oid)
    return CommonResult.successDictData("rating by order", resp_data)
@rating_api.post("/new")
def newRating():
    a_uid = get_member_login_id()
    if not a_uid:
        raise APIAuthFailed
    req = request.values
    oid = int(req['id']) if 'id' in req else None
    score = int(req['score']) if 'score' in req else -1
    content = req['content'] if 'content' in req else None
    illustration = req['illustration'] if 'illustration' in req else ''

    if oid is None:
        raise APIParameterException("请输入符合规范的姓名")
    if score < 1:
        raise APIParameterException("请输入符合规范评分")
    if content is None or len(content) < 2:
        raise APIParameterException("请输入符合规范的评论")
    order = orderService.ops({'id': oid, 'act': 'rating'})
    ratingService.newRating(a_uid,order.sid, oid, score, content, illustration)

    return CommonResult.success()
