# -*- coding: utf-8 -*-
# @Time : 2022/5/4 18:35
# @Author : Vincent Vic
# @File : MemberService.py
# @Software: PyCharm
import hashlib
import json

import requests
from application import db
from common.lib.Helper import getCurrentDate
from common.lib.Response import Response
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

    def login(self, code, nickName, avatarUrl, gender, client_type):
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
            .format(MINA_APP.appid, MINA_APP.appkey, code)
        r = requests.get(url)
        wx_resp = json.loads(r.text)
        # 存在errcode 且不是0说明请求失败
        if 'errcode' in wx_resp and wx_resp['errcode'] != 0:
            return Response.failMsg("微信登入失败:" + wx_resp['errmsg'])
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

        else:
            member = Member.query.filter_by(id=omb.member_id).first()
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

        return Response.successData("登入成功", info)
