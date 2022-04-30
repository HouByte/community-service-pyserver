# -*- coding: utf-8 -*-
# @Time : 2022/4/30 18:58
# @Author : Vincent Vic
# @File : UserService.py
# @Software: PyCharm
import base64
import hashlib

from common.lib.CommonResponse import Response
from web.model.User import User


class UserService:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            # 如果__instance还没有值，就给__instance变量赋值
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            # 如果__instance有值，则直接返回。
            return cls.__instance

    def login(self, data):
        user_info = User.query.filter_by(login_name=data['login_name']).first()
        if not user_info:
            return Response.failMsg("请输入正确的用户名或密码")
        if user_info.login_pwd != self.genePwd(data['login_pwd'], user_info.login_salt):
            return Response.failMsg("请输入正确的用户名或密码")
        token = "%s#%s" % (self.geneAuthCode(user_info), user_info.uid)
        return Response.successData("登入成功", token)

    def geneAuthCode(self, user_info):
        m = hashlib.md5()
        str = "%s-%s-%s-%s" % (user_info.uid, user_info.login_name, user_info.login_pwd, user_info.login_salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    def genePwd(selfo, pwd, salt):
        m = hashlib.md5()
        str = "%s-%s" % (base64.encodebytes(pwd.encode("utf-8")), salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()
