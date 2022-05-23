# -*- coding: utf-8 -*-
# @Time : 2022/4/30 9:02
# @Author : Vincent Vic
# @File : application.py
# @Software: PyCharm
import os

import redis
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

from common.lib.APIException import APIException
from common.lib.Helper import ops_render
from common.lib.UrlManager import UrlManager

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.flaskenv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = -1
# 基础配置加载
app.config.from_pyfile('config/base_setting.py')
# 数据库加载
app.config.from_pyfile('config/database_setting.py')
# 加载对应环境配置
env = os.getenv('FLASK_ENV', 'development')
app.config.from_pyfile('config/%s_setting.py' % env)

# 创建数据操作对象
db = SQLAlchemy(app, engine_options={
    'echo': True,
    'max_overflow': -1,
    'pool_size': 50,
    'pool_recycle': 8000,
    'pool_pre_ping': True
})


redis_host = app.config['REDIS_HOST']
redis_port = app.config['REDIS_PORT']
redis_db = app.config['REDIS_DB']
r_db = redis.StrictRedis(redis_host, redis_port, redis_db)

# 模板全局方法
app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl, 'buildUrl')


@app.errorhandler(Exception)
def all_page_exception_handler(e):
    path = request.path

    if isinstance(e, APIException):
        e.code
        return jsonify(code=e.code, msg=e.msg), e.code  # 这些异常类在 Werkzeug 中定义，均继承 HTTPException 类
    # 对于 HTTP 异常，返回自带的错误描述和状态码
    # 这些异常类在 Werkzeug 中定义，均继承 HTTPException 类
    if isinstance(e, HTTPException):
        if path.startswith("/api"):
            return jsonify(code=e.code, msg="请求异常请稍后再试"), e.code
        return ops_render('error/error.html'), e.code
    print(e)
    if path.startswith("/api"):
        return jsonify(code=e.code, msg="服务器异常请稍后再试"), 500
    return ops_render('error/error.html'), 500  # 一般异常
