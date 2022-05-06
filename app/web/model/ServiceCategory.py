# coding: utf-8
from application import db


class ServiceCategory(db.Model):
    __tablename__ = 'service_category'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue(), info='类别名称')
    weight = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='权重')
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='1:有效  0：无效')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='最后一次跟新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='插入时间')

    def keys(self):
        return ['id', 'name', 'weight', 'status', 'created_time', 'updated_time']

    def __getitem__(self, item):
        return getattr(self, item)
