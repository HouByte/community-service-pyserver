# -*- coding: utf-8 -*-
# @Time : 2022/4/30 13:02
# @Author : Vincent Vic
# @File : StaticController.py
# @Software: PyCharm

from flask import Blueprint, send_from_directory
from application import app

page_static = Blueprint('static', __name__)


@page_static.route("/<path:filename>")
def index(filename):
    return send_from_directory(app.root_path + "/static/", filename)
