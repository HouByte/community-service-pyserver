# -*- coding: utf-8 -*-
# @Time : 2022/4/30 18:58
# @Author : Vincent Vic
# @File : UserService.py
# @Software: PyCharm
import base64
import hashlib

from sqlalchemy import or_

from application import db
from common.lib.APIException import APIAuthFailed, APIForbidden, APIParameterException
from common.lib.Helper import Pagination, getCurrentDate
from common.lib.Utils import getRandomKey
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
            raise APIAuthFailed('请输入正确的用户名或密码')
            # return CommonResult.failMsg("请输入正确的用户名或密码")
        if user_info.login_pwd != self.genePwd(data['login_pwd'], user_info.login_salt):
            raise APIAuthFailed('请输入正确的用户名或密码')
            # return CommonResult.failMsg("请输入正确的用户名或密码")
        if user_info.status == 0:
            raise APIAuthFailed("账号被冻结~")
        return user_info

    def getInfoJson(self, user_info):
        info = {
            'uid': user_info.uid,
            'nickname': user_info.nickname,
            'mobile': user_info.mobile,
            'email': user_info.email,
            'sex': user_info.sex,
            'avatar': user_info.avatar,
            'login_name': user_info.login_name,
        }
        return info

    def getUserList(self, page_params):
        query = User.query
        # 分页处理
        page_params['total'] = query.count()
        pages = Pagination(page_params)
        mix_kw = page_params['mix_kw']
        # 昵称或手机号码查询
        if mix_kw != '':
            rule = or_(User.nickname.ilike("%{0}%".format(mix_kw)), User.mobile.ilike("%{0}%".format(mix_kw)))
            query = query.filter(rule)
        # 状态查询
        if int(page_params["status"]) > -1:
            query = query.filter(User.status == int(page_params["status"]))

        userList = query.order_by(User.uid.asc()).all()[pages.getOffset():pages.getLimit()]
        resp_data = {
            'list': userList,
            "pages": pages.getPages(),
        }
        return resp_data

    def getUserInfo(self, uid):
        user_info = User.query.filter_by(uid=uid).first()
        if user_info == None:
            return user_info
        user_info.login_pwd = ''
        user_info.login_salt = ''

        return user_info

    def getUser(self, uid):
        user_info = User.query.filter_by(uid=uid).first()
        if user_info is None:
            return user_info
        return user_info

    def edit(self, user_info):
        # 如果是新用户
        if not user_info.uid:
            user_info.created_time = getCurrentDate()
        user_info.updated_time = getCurrentDate()
        db.session.add(user_info)
        db.session.commit()

    def set(self, data):
        has_in = User.query.filter(User.login_name == data['login_name'], User.uid != data['uid']).first()
        if has_in:
            raise APIForbidden("该登录名已存在，请换一个试试~~")

        user_info = User.query.filter_by(uid=data['uid']).first()
        # 用户存在的情况下
        if user_info:
            model_user = user_info
            # 如果存在密码更新
            login_pwd = data['login_pwd']
            if login_pwd and len(login_pwd) > 6:
                model_user.login_pwd = self.genePwd(data['login_pwd'], model_user.login_salt)
        else:
            model_user = User()
            model_user.created_time = getCurrentDate()
            model_user.login_salt = self.geneSalt()
            model_user.login_pwd = self.genePwd(data['login_pwd'], model_user.login_salt)
        model_user.login_name = data['login_name']
        model_user.nickname = data['nickname']
        model_user.mobile = data['mobile']
        model_user.email = data['email']
        model_user.sex = data['sex']

        # 修改或新增
        self.edit(model_user)
        return model_user

    def updatePwd(self, user_info, new_password):
        user_info.updated_time = getCurrentDate()
        user_info.login_pwd = self.genePwd(new_password, user_info.login_salt)
        # 数据库修改
        db.session.add(user_info)
        db.session.commit()

    def resetPwd(self, user_info, data):
        if user_info.login_pwd != self.genePwd(data['old_password'], user_info.login_salt):
            raise APIParameterException("原密码不正确")
        if self.genePwd(data['new_password'], user_info.login_salt) == self.genePwd(data['old_password'], user_info.login_salt):
            raise APIParameterException("新密码不能与原密码相同")
        # 更新密码
        self.updatePwd(user_info, data['new_password'])

    def remove(self, uid):
        db.session.query(User).filter(User.uid == uid).delete()
        db.session.commit()

    def ops(self, data):
        act = data['act']
        uid = data['id']
        user_info = self.getUserInfo(uid)
        if not user_info:
            raise APIParameterException("用户不存在")
        if act == 'remove':
            self.remove(uid)
        elif act == 'lock':
            self.updateStatus(uid, 0)
        elif act == 'recover':
            self.updateStatus(uid, 1)
        db.session.commit()
        return user_info

    def updateStatus(self, uid, status):
        db.session.query(User).filter_by(uid=uid).update({'status': status, 'updated_time': getCurrentDate()})

    def geneAuthCode(self, user_info):
        m = hashlib.md5()
        str = "%s-%s-%s-%s" % (user_info.uid, user_info.login_name, user_info.login_pwd, user_info.login_salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    def genePwd(self, pwd, salt):
        m = hashlib.md5()
        str = "%s-%s" % (base64.encodebytes(pwd.encode("utf-8")), salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    def geneSalt(self, n=8):
        return getRandomKey(n)
