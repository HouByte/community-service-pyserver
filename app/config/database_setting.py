# -*- coding: utf-8 -*-
# @Time : 2022/4/30 8:57
# @Author : Vincent Vic
# @File : base_setting.py
# @Software: PyCharm
import os

# DATABASE 配置
DATABASE_TYPE = os.getenv('DATABASE_TYPE') or "mysql"
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME') or "root"
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD') or "root"
DATABASE_HOST = os.getenv('DATABASE_HOST') or "127.0.0.1"
DATABASE_PORT = int(os.getenv('DATABASE_PORT') or 3306)
DATABASE = os.getenv('DATABASE') or "PearAdminFlask"
SQLALCHEMY_DATABASE_URI = f'{DATABASE_TYPE}://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE}?useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Shanghai'
SQLALCHEMY_TRACK_MODIFICATIONS = False