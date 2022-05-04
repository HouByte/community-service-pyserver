# -*- coding: utf-8 -*-
# @Time : 2022/4/30 12:20
# @Author : Vincent Vic
# @File : __init__.py.py
# @Software: PyCharm
from application import app

# 蓝图管理
from web.controller.api.IndexApiController import index_api

app.register_blueprint(index_api, url_prefix="/api")
