# -*- coding: utf-8 -*-
# @Time : 2022/4/30 14:08
# @Author : Vincent Vic
# @File : AccountController.py
# @Software: PyCharm

from flask import Blueprint
from common.lib.Helper import ops_render

page_account = Blueprint('account_page', __name__)

@page_account.route("/index")
def index():
    return ops_render('account/index.html')

@page_account.route("/info")
def info():
    return ops_render('account/info.html')


@page_account.route("/set")
def set():
    return ops_render('account/set.html')