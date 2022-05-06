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
from common.lib.constant import API_TOKEN_KEY_REDIS, API_UID_KEY_REDIS
from common.lib.redis import Redis
from config.wexin_setting import MINA_APP
from web.model.Member import Member
from web.model.OauthMemberBind import OauthMemberBind
from web.model.ServiceCategory import ServiceCategory


class CategoryService:
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

    def getCategory(self,cid):
        return  ServiceCategory.query.filter_by(id=cid).first()


    def getCategoryList(self, page_params):
        query = ServiceCategory.query
        # 分页处理
        page_params['total'] = query.count()
        pages = Pagination(page_params)
        mix_kw = page_params['mix_kw']
        # 昵称或手机号码查询
        if mix_kw != '':
            rule = or_(ServiceCategory.nickname.ilike("%{0}%".format(mix_kw)), ServiceCategory.mobile.ilike("%{0}%".format(mix_kw)))
            query = query.filter(rule)
        # 状态查询
        if int(page_params["status"]) > -1:
            query = query.filter(ServiceCategory.status == int(page_params["status"]))

        categoryList = query.order_by(ServiceCategory.id.asc()).all()[pages.getOffset():pages.getLimit()]
        resp_data = {
            'list': categoryList,
            "pages": pages.getPages(),
        }
        return resp_data

    def selectOptions(self):
        categorys = ServiceCategory.query.filter(ServiceCategory.status == 1).order_by(ServiceCategory.weight.desc()).all()
        option = []
        for category in categorys:
            option.append({
                'id': category.id,
                'name': category.name
            })
        return option

    def idMaps(self):
        categorys = ServiceCategory.query.filter(ServiceCategory.status == 1).order_by(ServiceCategory.weight.desc()).all()
        map = dict()
        for category in categorys:
            map[category.id] = category.name
        return map

    def ops(self, data):
        act = data['act']
        mid = data['id']
        category = self.getCategory(mid)
        if not category:
            raise APIParameterException("分类不存在")
        if act == 'remove':
            self.remove(mid)
        elif act == 'lock':
            self.updateStatus(mid, 0)
        elif act == 'recover':
            self.updateStatus(mid, 1)
        db.session.commit()

    def updateStatus(self, mid, status):
        db.session.query(ServiceCategory).filter_by(id=mid).update({'status': status, 'updated_time': getCurrentDate()})

    def remove(self, cid):
        db.session.query(ServiceCategory).filter(ServiceCategory.id == cid).delete()
        db.session.commit()

    def edit(self, category):
        db.session.add(category)
        db.session.commit()
