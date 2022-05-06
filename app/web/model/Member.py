# coding: utf-8
from application import db


class Member(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(108), nullable=False, server_default=db.FetchedValue(), info='会员名')
    mobile = db.Column(db.String(11), nullable=True, server_default=db.FetchedValue(), info='会员手机号码')
    gender = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='1:男 2：女 0：没填写')
    avatar = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue(), info='会员头像')
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='1:有效 0：无效')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='最后一次时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='插入时间')

    def keys(self):
        return ['id', 'nickname', 'mobile', 'gender', 'avatar', 'status', 'updated_time', 'created_time']

    def __getitem__(self, item):
        return getattr(self, item)
