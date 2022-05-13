# coding: utf-8
from application import db


class ServiceOrder(db.Model):
    __tablename__ = 'service_order'

    id = db.Column(db.Integer, primary_key=True, info='id')
    orderNo = db.Column(db.String(20), nullable=False, info='订单id')
    status = db.Column(db.Integer, nullable=False, info='状态')
    p_uid = db.Column(db.Integer, nullable=False, info='提供者id')
    c_uid = db.Column(db.Integer, nullable=False, info='客户id')
    snap_title = db.Column(db.String(100), nullable=False, info='服务名称镜像')
    snap_nature = db.Column(db.Integer, nullable=False, info='性质：0 互助，1 服务，2 公益')
    snap_cover_image = db.Column(db.String(255), nullable=False, info='服务封面镜像')
    price = db.Column(db.Numeric(10, 2), nullable=False, info='订单金额')
    snap_price = db.Column(db.Numeric(10, 2), nullable=False, info='服务价格镜像')
    snap_category = db.Column(db.Integer, nullable=False, info='分类')
    consumer_snap_username = db.Column(db.String(100), info='客户名字镜像')
    consumer_snap_tel = db.Column(db.String(14), info='客户电话镜像')
    consumer_snap_province = db.Column(db.String(50), info='客户省份镜像')
    consumer_snap_city = db.Column(db.String(20), info='客户城市镜像')
    consumer_snap_county = db.Column(db.String(50), info='客户区镜像')
    consumer_snap_description = db.Column(db.String(255), info='客户地址详情镜像')
    created = db.Column(db.DateTime, server_default=db.FetchedValue(), info='创建时间')
    updated = db.Column(db.DateTime, server_default=db.FetchedValue(), info='更新时间')

    def keys(self):
        return ['id', 'orderNo', 'status', 'p_uid', 'c_uid', 'snap_title', 'snap_nature', 'snap_cover_image',
                'snap_price', 'snap_category', 'consumer_snap_username', 'consumer_snap_tel', 'consumer_snap_province',
                'consumer_snap_city', 'consumer_snap_county', 'consumer_snap_description', 'created', 'updated']

    def __getitem__(self, item):
        return getattr(self, item)

    def toJson(self):
        return {
            "orderNo": self.orderNo,
            "snap_title": self.snap_title,
            "snap_price": str(self.snap_price),
            "snap_cover_image": self.snap_cover_image,
            "snap_nature": self.snap_nature,
            "status": self.status,
            "snap_category": self.snap_category,
            "consumer_snap_username": self.consumer_snap_username,
            "consumer_snap_tel": self.consumer_snap_tel,
            "consumer_snap_province": self.consumer_snap_province,
            "consumer_snap_city": self.consumer_snap_city,
            "consumer_snap_county": self.consumer_snap_county,
            "consumer_snap_description": self.consumer_snap_description,
        }