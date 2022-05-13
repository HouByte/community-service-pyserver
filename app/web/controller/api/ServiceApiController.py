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
from web.model.Service import Service
from web.service.CategoryService import CategoryService
from web.service.MemberService import MemberService
from web.service.SService import SService

service_api = Blueprint('service_api', __name__)

sService = SService()
categoryService = CategoryService()
memberService = MemberService()


@service_api.get("/list")
def list():
    req = request.args
    page_params = getPageParams(req, app)
    # 我的页面查询需要登入
    source = int(req.get('source', 2))
    if source == 2:
        p_uid = get_member_login_id()
        if not p_uid:
            raise APIAuthFailed
        page_params['p_uid'] = p_uid
    page_params['source'] = 2
    page_params['api'] = True
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
            'id': service.category,
            'name': categoryMap[service.category]
        }
        member = memberService.getMember(service.p_uid)
        item['publisher'] = {
            'avatarUrl': member.avatar if member is not None else '',
            'nickname': member.nickname if member is not None else ''
        }
        item['beginDate'] = service.beginDate.strftime('%Y-%m-%d')
        item['endDate'] = service.endDate.strftime('%Y-%m-%d')
        list.append(item)
    resp_data['list'] = list

    return CommonResult.successDictData("list", resp_data)


@service_api.get("/desc")
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
        'id': member.id if member is not None else -1,
        'avatarUrl': member.avatar if member is not None else '',
        'nickname': member.nickname if member is not None else ''
    }
    return CommonResult.successDictData("desc", resp_data)


@service_api.get("/status/my")
def getStatus():
    mid = get_member_login_id()
    req = request.args
    type = req.get('type', -1)
    resp_data = sService.statusData(mid, type)
    return CommonResult.successDictData("desc", resp_data)


# beginDate: "2022-05-13"
# categoryId: 1
# coverImageUri: "upload/1652412964.png"
# description: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# designatedPlace: true
# endDate: "2022-05-15"
# id: undefined
# nature: 0
# price: "1111"
# title: "xxxxxxxxxxxxxxxx"
# type: 1
@service_api.post("/publish")
def publishService():
    p_uid = get_member_login_id()
    if not p_uid:
        raise APIAuthFailed
    req = request.values
    id = int(req['id']) if 'id' in req else None
    title = req['title'] if 'title' in req else None
    type = int(req['type']) if 'type' in req else -1
    nature = int(req['nature']) if 'nature' in req else -1
    price = float(req['price']) if 'price' in req else 0
    designatedPlace = req['designatedPlace'] if 'designatedPlace' in req else 0
    description = req['description'] if 'description' in req else None
    coverImage = req['coverImage'] if 'coverImage' in req else None
    category = int(req['categoryId']) if 'categoryId' in req else -1
    beginDate = req['beginDate'] if 'beginDate' in req else None
    endDate = req['endDate'] if 'endDate' in req else None
    if title is None or len(title) < 5:
        raise APIParameterException("请输入符合规范的标题")
    if type is None or type < 0:
        raise APIParameterException("请选择类型")
    if nature is None or nature < 0:
        raise APIParameterException("请选择性质")
    if description is None or len(description) < 20:
        raise APIParameterException("请输入符合规范的详情")
    if coverImage is None or len(coverImage) < 1 or coverImage == 'null':
        raise APIParameterException("请上传封面")
    if category is None or category < 0:
        raise APIParameterException("请选择分类")
    if nature == 1 and price <= 0:
        raise APIParameterException("请输入价格且大于0")

    params = {
        'title': title,
        'type': type,
        'nature': nature,
        'price': price,
        'designatedPlace': designatedPlace,
        'description': description,
        'coverImage': coverImage,
        'category': category,
        'beginDate': beginDate,
        'endDate': endDate,
        'p_uid': p_uid
    }

    if id is not None:
        params['id'] = id
    sService.publishService(params)
    return CommonResult.successMsg("提交成功")
