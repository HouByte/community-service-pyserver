# -*- coding: utf-8 -*-
# @Time : 2022/4/30 19:48
# @Author : Vincent Vic
# @File : Utils.py
# @Software: PyCharm
import json


def ObjToJson(obj):
    return json.dumps(obj, default=lambda obj: obj.__dict__, indent=4, sort_keys=True, ensure_ascii=False)