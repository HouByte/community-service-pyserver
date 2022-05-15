# -*- coding: utf-8 -*-
# @Time : 2022/5/14 15:38
# @Author : Vincent Vic
# @File : RatingService.py
# @Software: PyCharm
from application import db
from common.lib.Helper import getCurrentDate, Pagination
from web.model.Rating import Rating
from web.service.MemberService import MemberService

memberService = MemberService()


class RatingService:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            # 如果__instance还没有值，就给__instance变量赋值
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            # 如果__instance有值，则直接返回。
            return cls.__instance

    def newRating(self, mid, sid, oid, score, content, illustration):
        rating = Rating()
        rating.oid = oid
        rating.sid = sid
        rating.mid = mid
        rating.content = content
        rating.score = score
        rating.illustration = illustration
        rating.created = getCurrentDate()
        db.session.add(rating)
        db.session.commit()

    def getRatingList(self, page_params):
        query = Rating.query
        # 分页处理

        if int(page_params['sid']) > 0:
            query = query.filter(Rating.sid == int(page_params['sid']))
            page_params['total'] = query.filter(Rating.sid == int(page_params['sid'])).count()

        pages = Pagination(page_params)
        rating_list = query.order_by(Rating.id.desc()).all()[pages.getOffset():pages.getLimit()]
        resp_data = {
            'list': rating_list,
            "pages": pages.getPages(),
        }
        return resp_data

    def getRatingByOrder(self, oid):
        rating = Rating.query.filter(Rating.oid == oid).first()
        return self.toVo(rating)

    def toVo(self, rating):
        item = dict();
        member = memberService.getMember(rating.mid)
        item['id'] = rating.id
        item['score'] = rating.score
        item['content'] = rating.content
        if len(rating.illustration) >0:
            item['illustration'] = rating.illustration.split(",")
        item['created'] = rating.created.strftime('%Y-%m-%d')
        item['author'] = {
            'nickname': member.nickname,
            'avatarUrl': member.avatar
        }

        return item
