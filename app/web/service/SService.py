# -*- coding: utf-8 -*-
# @Time : 2022/5/4 18:35
# @Author : Vincent Vic
# @File : CategoryService.py
# @Software: PyCharm

from sqlalchemy import or_

from application import db
from common.lib.APIException import APIParameterException
from common.lib.Helper import getCurrentDate, Pagination
from common.lib.constant import serviceStatus
from web.model.Service import Service
from web.service.UserService import UserService

userService = UserService()


class SService:
    __instance = None

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

        mix_kw = page_params['mix_kw']
        # 昵称或手机号码查询
        if mix_kw != '':
            rule = or_(Service.title.ilike("%{0}%".format(mix_kw)), Service.description.ilike("%{0}%".format(mix_kw)))
            query = query.filter(rule)
        p_uid = int(page_params["p_uid"]) if 'p_uid' in page_params else -1
        openApi = True if 'api' in page_params else False
        print(p_uid)

        # 状态查询,状态大于-1 且 不是公开api可以查询 (后台)
        if int(page_params["status"]) > -1 and not openApi:
            page_params['total'] = query.filter(Service.status == int(page_params["status"])).count()
            query = query.filter(Service.status == int(page_params["status"]))  # 状态查询
        # 状态查询,小程序查询 状态大于-1 且 会员id存在 （小程序查询自己的服务）
        elif openApi and int(page_params["status"]) > -1 and p_uid > 0:
            page_params['total'] = query.filter(Service.status == int(page_params["status"])).count()
            query = query.filter(Service.status == int(page_params["status"]))  # 状态查询
            query = query.filter(Service.p_uid == p_uid)
        # 小程序查询
        elif openApi:
            page_params['total'] = query.filter(Service.status == serviceStatus.PUBLISHED).count()
            query = query.filter(Service.status == serviceStatus.PUBLISHED)  # 公开状态查询

        if int(page_params["nature"]) > -1:
            query = query.filter(Service.nature == int(page_params["nature"]))
        if int(page_params["type"]) > -1:
            query = query.filter(Service.type == int(page_params["type"]))
        if int(page_params["category_id"]) > -1:
            query = query.filter(Service.category == int(page_params["category_id"]))

        pages = Pagination(page_params)
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
        elif act == 'off_shelves':
            self.updateStatus(sid, serviceStatus.OFF_SHELVES)
        elif act == 'approval':
            self.updateStatus(sid, serviceStatus.PUBLISHED)
        elif act == 'refuse':
            self.updateStatus(sid, serviceStatus.DENY)
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

    def statusData(self, mid, type):

        data = {
            'unpublished': 0,
            'pending': 0,
            'published': 0,
            'all': 0
        }

        if not mid:
            return data
        query = Service.query
        if int(type) >= 0:
            query = query.filter(Service.type == type)
        list = query.filter(Service.p_uid == mid).all()
        data['all'] = len(list)
        for item in list:
            # 未发布和被拒绝，取消都算
            if item.status == serviceStatus.UNPUBLISHED or item.status == serviceStatus.DENY or \
                    item.status == serviceStatus.OFF_SHELVES:
                data['unpublished'] = data['unpublished'] + 1
            elif item.status == serviceStatus.PUBLISHED:
                data['published'] = data['published'] + 1
            elif item.status == serviceStatus.PENDING:
                data['pending'] = data['pending'] + 1

        return data
