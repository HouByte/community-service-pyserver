# -*- coding: utf-8 -*-
# @Time : 2022/4/30 14:13
# @Author : Vincent Vic
# @File : MemberController.py
# @Software: PyCharm
from flask import Blueprint, render_template

page_member = Blueprint('member_page', __name__)


@page_member.route("/index")
def index():
    return render_template('member/index.html')


@page_member.route("/info")
def info():
    return render_template('member/info.html')


@page_member.route("/set")
def set():
    return render_template('member/set.html')
