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

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.flaskenv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Application(Flask):
    def __int__(self, import_name):
        super(Application, self).__init__(import_name)
        self.config.from_pyfile('config/base_setting.py')
        self.config.from_pyfile('config/database_setting.py')
        # 加载对应环境配置
        env = os.getenv('FLASK_ENV', 'development')
        self.config.from_pyfile('config/%s_setting.py' % env)
        db.init_app(self)


db = SQLAlchemy()
app = Application(__name__)
