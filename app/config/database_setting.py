# -*- coding: utf-8 -*-
# @Time : 2022/4/30 8:57
# @Author : Vincent Vic
# @File : base_setting.py
# @Software: PyCharm
import os

# DATABASE 配置
from datetime import timedelta

DATABASE_TYPE = os.getenv('DATABASE_TYPE') or "mysql"
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME') or "root"
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD') or "root"
DATABASE_HOST = os.getenv('DATABASE_HOST') or "127.0.0.1"
DATABASE_PORT = int(os.getenv('DATABASE_PORT') or 3306)
DATABASE = os.getenv('DATABASE') or "PearAdminFlask"
SQLALCHEMY_DATABASE_URI = f'{DATABASE_TYPE}://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE}'
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
SQLALCHEMY_POOL_SIZE = 50


# Redis 配置
REDIS_HOST = os.getenv('REDIS_HOST') or "127.0.0.1"
REDIS_PORT = int(os.getenv('REDIS_PORT') or 6379)
REDIS_DB = int(os.getenv('REDIS_DB') or 6379)
REDIS_EXPIRE = int(os.getenv('REDIS_EXPIRE') or 86400)