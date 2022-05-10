# -*- coding: utf-8 -*-
# @Time : 2022/4/30 19:01
# @Author : Vincent Vic
# @File : Response.py
# @Software: PyCharm
import json

from flask import jsonify

from application import db
from common.lib.Utils import ObjToJson


class CommonResult:


    @staticmethod
    def success():
        return jsonify(code=200, msg='success')

    @staticmethod
    def successMsg(msg):
        return jsonify(code=200, msg=msg)

    @staticmethod
    def successDictData(msg, data):
        return jsonify(code=200, msg=msg,data=dict(data))

    @staticmethod
    def successData(msg, data):
        return jsonify(code=200, msg=msg,data=data)

    @staticmethod
    def fail():
        return jsonify(code=-1, msg='fail')

    @staticmethod
    def failMsg(msg):
        return jsonify(code=-1, msg=msg)

    @staticmethod
    def build(code, msg, data):
        return jsonify(code=code, msg=msg, data=jsonify(data))

    def toJson(self):
        return ObjToJson(self)

    def toSimpleJson(self):
        info = {
            'code':self.code,
            'msg':self.msg
        }
        return info

    def keys(self):
        return ['code', 'msg', 'data']

    def __getitem__(self, item):
        return getattr(self, item)
