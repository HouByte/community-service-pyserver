# -*- coding: utf-8 -*-
# @Time : 2022/4/30 19:01
# @Author : Vincent Vic
# @File : Response.py
# @Software: PyCharm
import json

from common.lib.Utils import ObjToJson


class Response:

    def __init__(self, code, msg, data=None):
        self.code = code
        self.msg = msg
        self.data = data

    @staticmethod
    def success():
        return Response(200, 'success')

    @staticmethod
    def successMsg(msg):
        return Response(200, msg)

    @staticmethod
    def successData(msg, data):
        return Response(200, msg, data)

    @staticmethod
    def fail():
        return Response(-1, 'fail')

    @staticmethod
    def failMsg(msg):
        return Response(-1, msg)

    @staticmethod
    def build(code, msg, data):
        return Response(code, msg, data)

    def toJson(self):
        return ObjToJson(self)

    def toSimpleJson(self):
        info = {
            'code':self.code,
            'msg':self.msg
        }
        return info

    def isSuccess(self):
        return  self.code == 200
