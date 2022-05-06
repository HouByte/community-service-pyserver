# coding: utf-8
from application import db

class User(db.Model):
    __tablename__ = 'user'

    uid = db.Column(db.BigInteger, primary_key=True, info='用户uid')
    nickname = db.Column(db.String(100), nullable=False, info='用户名')
    mobile = db.Column(db.String(20), nullable=False, info='手机号码')
    email = db.Column(db.String(100), nullable=False, info='邮箱')
    sex = db.Column(db.Integer, nullable=False, info='1:男,2:女,0:没填写')
    avatar = db.Column(db.String(64), nullable=False, info='头像')
    login_name = db.Column(db.String(20), nullable=False, unique=True, info='登录用户名')
    login_pwd = db.Column(db.String(32), nullable=False, info='登录密码')
    login_salt = db.Column(db.String(32), nullable=False, info='登录密码的随机加密秘钥')
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='1:有效,0:无效')
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='最后一次更新时间')
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='插入时间')

    def keys(self):
        return ['uid', 'nickname', 'mobile', 'email', 'sex', 'avatar', 'login_name', 'login_pwd', 'login_salt',
                'status', 'updated_time', 'created_time']

    def __getitem__(self, item):
        return getattr(self, item)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


