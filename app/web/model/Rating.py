# coding: utf-8
from application import db


class Rating(db.Model):
    __tablename__ = 'rating'

    id = db.Column(db.Integer, primary_key=True, info='id')
    oid = db.Column(db.Integer, nullable=False, info='订单id')
    sid = db.Column(db.Integer, nullable=False, info='服务id')
    mid = db.Column(db.Integer, nullable=False, info='会员id')
    content = db.Column(db.String(255), nullable=False, info='评论内容')
    score = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='评分')
    illustration = db.Column(db.String(255), info='图片')
    created = db.Column(db.Date, nullable=False, info='评论时间')
