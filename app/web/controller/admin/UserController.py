# -*- coding: utf-8 -*-
# @Time : 2022/4/30 12:22
# @Author : Vincent Vic
# @File : UserController.py
# @Software: PyCharm

from flask import Blueprint, render_template

page_user = Blueprint('user_page', __name__)


@page_user.route("/edit")
def edit():
    return render_template('user/edit.html')


@page_user.route("/reset-pwd")
def resetPwd():
    return render_template('user/reset-pwd.html')
