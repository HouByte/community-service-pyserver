# -*- coding: utf-8 -*-
# @Time : 2022/5/4 18:35
# @Author : Vincent Vic
# @File : CategoryService.py
# @Software: PyCharm

from sqlalchemy import or_

from application import db
from common.lib.APIException import APIParameterException
from common.lib.Helper import getCurrentDate, Pagination
from web.model.Service import Service
from web.service.UserService import UserService

userService = UserService()

class SService:
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

    def getService(self, sid):
        return Service.query.filter_by(id=sid).first()

    def getServiceInfo(self, sid):
        service = self.getService(sid)
        if not service:
            raise APIParameterException("服务不存在")
        info = dict(service)
        p_user = userService.getUser(service.p_uid)
        info['p_user'] = {
            'nickname': p_user.nickname if p_user is not None else '用户已注销'
        }
        return info

    def getServiceList(self, page_params):
        query = Service.query
        # 分页处理
        page_params['total'] = query.count()
        pages = Pagination(page_params)
        mix_kw = page_params['mix_kw']
        # 昵称或手机号码查询
        if mix_kw != '':
            rule = or_(Service.title.ilike("%{0}%".format(mix_kw)), Service.description.ilike("%{0}%".format(mix_kw)))
            query = query.filter(rule)
        # 状态查询
        if int(page_params["status"]) > -1:
            query = query.filter(Service.status == int(page_params["status"]))        # 状态查询
        if int(page_params["nature"]) > -1:
            query = query.filter(Service.nature == int(page_params["nature"]))
        if int(page_params["type"]) > -1:
            query = query.filter(Service.type == int(page_params["type"]))
        if int(page_params["category_id"]) > -1:
            query = query.filter(Service.category == int(page_params["category_id"]))

        serviceList = query.order_by(Service.id.asc()).all()[pages.getOffset():pages.getLimit()]
        resp_data = {
            'list': serviceList,
            "pages": pages.getPages(),
        }
        return resp_data

    def ops(self, data):
        act = data['act']
        sid = data['id']
        service = self.getService(sid)
        if not service:
            raise APIParameterException("服务不存在")
        if act == 'remove':
            self.remove(sid)
        elif act == 'lock':
            self.updateStatus(sid, 0)
        elif act == 'recover':
            self.updateStatus(sid, 1)
        db.session.commit()

    def updateStatus(self, sid, status):
        db.session.query(Service).filter_by(id=sid).update({'status': status, 'updated': getCurrentDate()})

    def remove(self, sid):
        db.session.query(Service).filter(Service.id == sid).delete()
        db.session.commit()

    def edit(self, service):
        service.updated = getCurrentDate()
        db.session.add(service)
        db.session.commit()
