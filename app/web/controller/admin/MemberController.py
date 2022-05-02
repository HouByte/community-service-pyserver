# -*- coding: utf-8 -*-
# @Time : 2022/4/30 14:13
# @Author : Vincent Vic
# @File : MemberController.py
# @Software: PyCharm
from flask import Blueprint
from common.lib.Helper import ops_render

page_member = Blueprint('member_page', __name__)


@page_member.route("/index")
def index():
    return ops_render('member/index.html')


@page_member.route("/info")
def info():
    return ops_render('member/info.html')


@page_member.route("/set")
def set():
    return ops_render('member/set.html')
