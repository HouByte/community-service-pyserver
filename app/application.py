# -*- coding: utf-8 -*-
# @Time : 2022/4/30 9:02
# @Author : Vincent Vic
# @File : application.py
# @Software: PyCharm
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from common.lib.UrlManager import UrlManager

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.flaskenv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 基础配置加载
app.config.from_pyfile('config/base_setting.py')
# 数据库加载
app.config.from_pyfile('config/database_setting.py')
# 加载对应环境配置
env = os.getenv('FLASK_ENV', 'development')
app.config.from_pyfile('config/%s_setting.py' % env)

# 创建数据操作对象
db = SQLAlchemy(app)

# 模板全局方法
app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl, 'buildUrl')
