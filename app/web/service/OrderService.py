# -*- coding: utf-8 -*-
# @Time : 2022/5/4 18:35
# @Author : Vincent Vic
# @File : CategoryService.py
# @Software: PyCharm
import hashlib
import json

import requests
from sqlalchemy import or_

from application import db
from common.lib.APIException import APIParameterException
from common.lib.Helper import getCurrentDate, Pagination
from common.lib.CommonResult import CommonResult
from web.model.ServiceOrder import ServiceOrder
from web.service.UserService import UserService

userService = UserService()

class OrderService:
    __instance = None

    omb_types = {
        'wechat_mini': 1
    }

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            # 如果__instance还没有值，就给__instance变量赋值
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            # 如果__instance有值，则直接返回。
            return cls.__instance

    def getService(self, id):
        return ServiceOrder.query.filter_by(id=id).first()

    def getServiceInfo(self, sid):
        serviceOrder = self.getService(sid)
        if not serviceOrder:
            raise APIParameterException("订单不存在")
        info = dict(serviceOrder)
        # p_user
        p_user = userService.getUser(serviceOrder.p_uid)
        info['p_user'] = {
            'nickname': p_user.nickname if p_user is not None else '用户已注销'
        }
        # c_user
        c_user = userService.getUser(serviceOrder.c_uid)
        info['c_user'] = {
            'nickname': c_user.nickname if c_user is not None else '用户已注销'
        }
        return info

    def getServiceList(self, page_params):
        query = ServiceOrder.query
        # 分页处理
        page_params['total'] = query.count()
        pages = Pagination(page_params)
        mix_kw = page_params['mix_kw']
        # 昵称或手机号码查询
        if mix_kw != '':
            rule = or_(ServiceOrder.nickname.ilike("%{0}%".format(mix_kw)), ServiceOrder.mobile.ilike("%{0}%".format(mix_kw)))
            query = query.filter(rule)
        # 状态查询
        if int(page_params["status"]) > -1:
            query = query.filter(ServiceOrder.status == int(page_params["status"]))

        if int(page_params["nature"]) > -1:
            query = query.filter(ServiceOrder.snap_nature == int(page_params["nature"]))

        serviceList = query.order_by(ServiceOrder.id.asc()).all()[pages.getOffset():pages.getLimit()]
        resp_data = {
            'list': serviceList,
            "pages": pages.getPages(),
        }
        return resp_data

    def ops(self, data):
        act = data['act']
        sid = data['id']
        serviceOrder = self.getService(sid)
        if not serviceOrder:
            raise APIParameterException("订单不存在")
        if act == 'remove':
            self.remove(sid)
        elif act == 'lock':
            self.updateStatus(sid, 0)
        elif act == 'recover':
            self.updateStatus(sid, 1)
        db.session.commit()

    def updateStatus(self, sid, status):
        db.session.query(ServiceOrder).filter_by(id=sid).update({'status': status, 'updated': getCurrentDate()})

    def remove(self, sid):
        db.session.query(ServiceOrder).filter(ServiceOrder.id == sid).delete()
        db.session.commit()

    def edit(self, serviceOrder):
        serviceOrder.updated = getCurrentDate()
        db.session.add(serviceOrder)
        db.session.commit()
