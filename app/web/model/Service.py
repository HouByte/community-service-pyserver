# coding: utf-8
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Service(db.Model):
    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True, info='id')
    status = db.Column(db.Integer, nullable=False, info='状态')
    type = db.Column(db.Integer, nullable=False, info='类型：1 找/ 2提供')
    nature = db.Column(db.Integer, nullable=False, info='性质：0 互助，1 服务，2 公益')
    title = db.Column(db.String(100), nullable=False, info='标题')
    description = db.Column(db.String, info='详情')
    coverImage = db.Column(db.String(255), nullable=False, info='封面')
    designatedPlace = db.Column(db.Integer, info='指定地点')
    price = db.Column(db.Numeric(10, 2), nullable=False, info='价格，互助和公益为0')
    p_uid = db.Column(db.Integer, nullable=False, info='发布人id')
    category = db.Column(db.Integer, nullable=False, info='分类')
    salesVolume = db.Column(db.Integer, info='使用量')
    score = db.Column(db.Integer, info='评分')
    created = db.Column(db.DateTime, server_default=db.FetchedValue(), info='创建时间')
    updated = db.Column(db.DateTime, server_default=db.FetchedValue(), info='更新时间')
    beginDate = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='服务开始时间')
    endDate = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='服务结束时间')

    def keys(self):
        return ['id', 'type', 'nature', 'title', 'description', 'coverImage', 'designatedPlace', 'price', 'p_uid', 'category',
                'status', 'salesVolume', 'score', 'created', 'updated', 'beginDate', 'endDate']

    def __getitem__(self, item):
        return getattr(self, item)

    def toJson(self):
        return {
            "title": self.title,
            "designatedPlace": self.designatedPlace,
            "price": str(self.price),
            "description": self.description,
            "nature": self.nature,
            "status": self.status,
            "category": self.category,
            "salesVolume": self.salesVolume,
            "score": self.score,
            "beginDate": str(self.beginDate),
            "endDate": str(self.endDate),
        }
