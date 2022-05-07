# -*- coding: utf-8 -*-
# @Time : 2022/4/30 14:13
# @Author : Vincent Vic
# @File : CategoryController.py
# @Software: PyCharm
from flask import Blueprint, request

from application import app
from common.lib.APIException import APIParameterException
from common.lib.CommonResult import CommonResult
from common.lib.Helper import ops_render, getOpsData, getPageParams
from web.service.CategoryService import CategoryService
from web.service.OrderService import OrderService

page_order = Blueprint('order_page', __name__)
orderService = OrderService()
categoryService=CategoryService()

@page_order.route("/index")
def index():
    req = request.args
    page_params = getPageParams(req, app)
    resp_data = orderService.getServiceList(page_params)
    resp_data["status_mapping"] = app.config["STATUS_MAPPING"]
    resp_data["nature_mapping"] = app.config["NATURE_MAPPING"]
    resp_data['categorys'] = categoryService.selectOptions()
    resp_data['categoryMap'] = categoryService.idMaps()
    resp_data["search_con"] = req
    return ops_render('order/index.html', resp_data)


@page_order.route("/info", methods=["POST"])
def info():
    req = request.values
    id = req['id'] if 'id' in req else None
    if not id:
        raise APIParameterException("参数错误")
    info = orderService.getServiceInfo(id)
    return CommonResult.successData("信息", info)


@page_order.route("/ops", methods=["POST"])
def ops():
    data = getOpsData(request.values)
    if not data['act'] or not data['id']:
        raise APIParameterException("参数错误")
    orderService.ops(data)
    return CommonResult.successMsg("更新成功")
