# -*- coding: utf-8 -*-
# @Time : 2022/4/30 14:13
# @Author : Vincent Vic
# @File : CategoryController.py
# @Software: PyCharm
from flask import Blueprint, request

from application import app
from common.lib.APIException import APIParameterException
from common.lib.Helper import ops_render, getOpsData, getPageParams
from common.lib.CommonResult import CommonResult
from common.lib.constant import API_UID_KEY_REDIS, API_TOKEN_KEY_REDIS
from common.lib.redis import Redis
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
    if not data['act'] or not data['id']:
        raise APIParameterException("参数错误")
    categoryService.ops(data)
    return CommonResult.successMsg("更新成功")
