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

page_category = Blueprint('category_page', __name__)
categoryService = CategoryService()


@page_category.route("/index")
def index():
    req = request.args
    page_params = getPageParams(req, app)
    resp_data = categoryService.getCategoryList(page_params)
    resp_data["status_mapping"] = app.config["STATUS_MAPPING"]
    resp_data["search_con"] = req
    return ops_render('category/index.html', resp_data)


@page_category.route("/ops", methods=["POST"])
def ops():
    data = getOpsData(request.values)
    categoryService.ops(data)
    return CommonResult.successMsg("更新成功")


@page_category.route("/set", methods=["GET", "POST"])
def set():
    if request.method == 'GET':
        req = request.args
        id = int(req.get('id', -1))
        if id > 0:
            info = categoryService.getCategory(id)
        if id < 1 or not info:
            info = {
                'name': '',
                'weight': 0
            }
        resp_data = {
            "category": info
        }
        return ops_render('category/set.html', resp_data)
    req = request.values
    id = int(req['id'] if 'id' in req else -1)
    name = req['name'] if 'name' in req else ''
    weight = req['weight'] if 'weight' in req else 0

    if weight is None or len(weight) < 1:
        raise APIParameterException("请输入符合规范的分类名称")

    data = {
        'id': id,
        'name': name,
        'weight': weight
    }
    categoryService.set(data)

    return CommonResult.successMsg("更新成功")