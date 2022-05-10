# -*- coding: utf-8 -*-
# @Time : 2022/4/30 12:22
# @Author : Vincent Vic
# @File : UserController.py
# @Software: PyCharm
from flask import Blueprint

from common.lib.CommonResult import CommonResult
from web.service.CategoryService import CategoryService

category_api = Blueprint('category_api', __name__)

categoryService = CategoryService()


@category_api.route("/select/options")
def selectOptions():
    resp_data = categoryService.selectOptions()
    return CommonResult.successData("selectOptions", resp_data)


@category_api.route("/id/maps")
def idMaps():
    resp_data = categoryService.idMaps()
    return CommonResult.successData("selectOptions", resp_data)