# -*- coding: utf-8 -*-
# @Time : 2022/4/30 14:08
# @Author : Vincent Vic
# @File : AccountController.py
# @Software: PyCharm

from flask import Blueprint, render_template

page_account = Blueprint('account_page', __name__)

@page_account.route("/index")
def index():
    return render_template('account/index.html')

@page_account.route("/info")
def info():
    return render_template('account/info.html')


@page_account.route("/set")
def set():
    return render_template('account/set.html')