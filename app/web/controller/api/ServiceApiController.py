# -*- coding: utf-8 -*-
# @Time : 2022/4/30 12:22
# @Author : Vincent Vic
# @File : UserController.py
# @Software: PyCharm
from flask import Blueprint, request

from application import app
from common.lib.APIException import APIParameterException
from common.lib.CommonResult import CommonResult
from common.lib.Helper import getPageParams
from web.service.CategoryService import CategoryService
from web.service.MemberService import MemberService
from web.service.SService import SService

service_api = Blueprint('service_api', __name__)

sService = SService()
categoryService = CategoryService()
memberService = MemberService()

@service_api.route("/list")
def list():
    req = request.args
    page_params = getPageParams(req, app)
    resp_data = sService.getServiceList(page_params)
    pages = resp_data['pages']
    resp_data['pages'] = {
        'page_size': pages['page_size'],
        'total': pages['total'],
        'is_next': pages['is_next']
    }
    list = []
    service_list = resp_data['list']
    categoryMap = categoryService.idMaps()
    for service in service_list:
        item = dict(service);
        item['category'] = {
            'id':service.category,
            'name': categoryMap[service.category]
        }
        member = memberService.getMember(service.p_uid)
        item['publisher'] = {
            'avatarUrl':member.avatar,
            'nickname': member.nickname
        }
        item['beginDate'] = service.beginDate.strftime('%Y-%m-%d')
        item['endDate'] = service.endDate.strftime('%Y-%m-%d')
        list.append(item)
    resp_data['list'] = list

    return CommonResult.successDictData("list", resp_data)

@service_api.route("/desc")
def getInfo():
    req = request.args
    id = int(req.get('id', -1))
    if id < 0:
        raise APIParameterException("参数错误")
    service = sService.getService(id)
    resp_data = dict(service)
    resp_data['beginDate'] = service.beginDate.strftime('%Y-%m-%d')
    resp_data['endDate'] = service.endDate.strftime('%Y-%m-%d')
    member = memberService.getMember(service.p_uid)
    resp_data['publisher'] = {
        'id': member.id,
        'avatarUrl': member.avatar,
        'nickname': member.nickname
    }
    return CommonResult.successDictData("desc", resp_data)