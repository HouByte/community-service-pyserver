# -*- coding: utf-8 -*-
# @Time : 2022/4/30 12:20
# @Author : Vincent Vic
# @File : __init__.py.py
# @Software: PyCharm
from web.controller.admin.AccountController import page_account
from web.controller.admin.CategoryController import page_category
from web.controller.admin.IndexController import page_index
from web.controller.admin.MemberController import page_member
from web.controller.admin.OrderController import page_order
from web.controller.admin.ServiceController import page_service
from web.controller.admin.StaticController import page_static
from web.controller.admin.UserController import page_user
from web.interceptors.AuthInterceptor import *

# 蓝图管理
app.register_blueprint(page_static, url_prefix="/static")
app.register_blueprint(page_index, url_prefix="/")
app.register_blueprint(page_user, url_prefix="/user")
app.register_blueprint(page_account, url_prefix="/account")
app.register_blueprint(page_member, url_prefix="/member")
app.register_blueprint(page_category, url_prefix="/category")
app.register_blueprint(page_service, url_prefix="/service")
app.register_blueprint(page_order, url_prefix="/order")
