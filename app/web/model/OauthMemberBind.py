# coding: utf-8
from application import db


class OauthMemberBind(db.Model):
    __tablename__ = 'oauth_member_bind'
    __table_args__ = (
        db.Index('idx_type_openid', 'type', 'openid'),
    )

    id = db.Column(db.Integer, primary_key=True, info='id')
    member_id = db.Column(db.Integer, nullable=False, info='会员id')
    client_type = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue(), info='客户端来源类型:web, wechat')
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='类型type 1:wechat ')
    openid = db.Column(db.String(80), info='第三方id ')
    unionid = db.Column(db.String(100), server_default=db.FetchedValue(), info='跨应用id')
    extra = db.Column(db.Text, nullable=False, info='额外字段')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='最后更新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='插入时间')

    def keys(self):
        return ['id', 'member_id', 'type', 'client_type', 'unionid', 'extra', 'openid', 'updated_time', 'created_time']

    def __getitem__(self, item):
        return getattr(self, item)
