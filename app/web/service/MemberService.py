# -*- coding: utf-8 -*-
# @Time : 2022/5/4 18:35
# @Author : Vincent Vic
# @File : MemberService.py
# @Software: PyCharm
import datetime
import hashlib
import json

import requests
from sqlalchemy import or_

from application import db
from common.lib.APIException import APIParameterException
from common.lib.Helper import getCurrentDate, Pagination, getDateByAgo
from common.lib.constant import API_TOKEN_KEY_REDIS, API_UID_KEY_REDIS
from common.lib.redis import Redis
from config.wexin_setting import MINA_APP
from web.model.Member import Member
from web.model.OauthMemberBind import OauthMemberBind


class MemberService:
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

    def getMember(self,mid):
        return  Member.query.filter_by(id=mid).first()


    def login(self, code, nickName, avatarUrl, gender, client_type):
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
            .format(MINA_APP.appid, MINA_APP.appkey, code)
        r = requests.get(url)
        wx_resp = json.loads(r.text)
        # 存在errcode 且不是0说明请求失败
        if 'errcode' in wx_resp and wx_resp['errcode'] != 0:
            raise APIParameterException("微信登入失败:" + wx_resp['errmsg'])
        openid = wx_resp['openid']
        session_key = wx_resp['session_key']

        # 查询是否有对应关系，有更新，没有新增
        omb = OauthMemberBind.query.filter_by(openid=openid).first()
        if omb is None:
            member = Member()
            member.nickname = nickName
            member.avatar = avatarUrl
            member.gender = gender
            member.status = 1
            member.created_time = getCurrentDate()
            member.updated_time = getCurrentDate()
            db.session.add(member)
            db.session.flush()
            # 添加新关系
            omb = OauthMemberBind()
            omb.openid = openid
            omb.member_id = member.id
            omb.client_type = client_type
            omb.unionid = ''
            omb.extra = ''
            omb.type = self.omb_types[client_type]
            omb.created_time = getCurrentDate()
            omb.updated_time = getCurrentDate()
            db.session.add(omb)
            db.session.commit()
            db.session.close()

        else:
            member = self.getMember(omb.member_id)
            if member.status == 0:
                raise APIParameterException("用户被冻结，无法登入")
            member.nickname = nickName
            member.avatar = avatarUrl
            member.gender = gender
            member.updated_time = getCurrentDate()
            db.session.add(member)

        db.session.commit()

        token = hashlib.md5(session_key.encode(encoding='UTF-8')).hexdigest()
        info = {
            'token': token,
            'id': member.id
        }
        Redis.write(API_TOKEN_KEY_REDIS + token, json.dumps(info))
        Redis.write(API_UID_KEY_REDIS + str(member.id), token)

        return info

    def getMemberList(self, page_params):
        query = Member.query
        # 分页处理
        page_params['total'] = query.count()
        pages = Pagination(page_params)
        mix_kw = page_params['mix_kw']
        # 昵称或手机号码查询
        if mix_kw != '':
            rule = or_(Member.nickname.ilike("%{0}%".format(mix_kw)), Member.mobile.ilike("%{0}%".format(mix_kw)))
            query = query.filter(rule)
        # 状态查询
        if int(page_params["status"]) > -1:
            query = query.filter(Member.status == int(page_params["status"]))

        memberList = query.order_by(Member.id.asc()).all()[pages.getOffset():pages.getLimit()]
        resp_data = {
            'list': memberList,
            "pages": pages.getPages(),
        }
        return resp_data

    def ops(self, data):
        act = data['act']
        mid = data['id']
        member = self.getMember(mid)
        if not member:
            raise APIParameterException("会员不存在")
        if act == 'remove':
            self.remove(mid)
        elif act == 'lock':
            self.updateStatus(mid, 0)
        elif act == 'recover':
            self.updateStatus(mid, 1)

        return member.id

    def updateStatus(self, mid, status):
        db.session.query(Member).filter_by(id=mid).update({'status': status, 'updated_time': getCurrentDate()})
        db.session.commit()

    def remove(self, mid):
        db.session.query(Member).filter(Member.id == mid).delete()
        db.session.commit()

    def edit(self, member):
        db.session.add(member)
        db.session.commit()

    def getVolume(self, day=30):
        q_date = getDateByAgo(day)
        list = Member.query.filter(Member.created_time >= q_date).all()
        resp_data = {
            'today-member-volume': 0,
            '30-member-volume': len(list),
        }
        for item in list:
            if item.created_time.strftime('%Y-%m-%d') == datetime.datetime.now().strftime('%Y-%m-%d'):
                resp_data['today-member-volume'] = resp_data['today-member-volume'] + 1

        return resp_data
