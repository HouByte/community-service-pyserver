# -*- coding: utf-8 -*-
# @Time : 2022/4/30 12:20
# @Author : Vincent Vic
# @File : __init__.py.py
# @Software: PyCharm
from application import app

# 蓝图管理
from web.controller.api.CategoryApiController import category_api
from web.controller.api.FileUploadApiController import file_upload_api
from web.controller.api.IndexApiController import index_api
from web.controller.api.OrderApiController import order_api
from web.controller.api.ServiceApiController import service_api

app.register_blueprint(index_api, url_prefix="/api")
app.register_blueprint(service_api, url_prefix="/api/service")
app.register_blueprint(category_api, url_prefix="/api/category")
app.register_blueprint(order_api, url_prefix="/api/order")
app.register_blueprint(file_upload_api, url_prefix="/api/upload")
