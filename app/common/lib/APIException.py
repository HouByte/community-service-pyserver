# -*- coding: utf-8 -*-
# @Time : 2022/5/6 21:26
# @Author : Vincent Vic
# @File : APIException.py
# @Software: PyCharm
from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = 'sorry, we made a mistake!'
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]

class APISuccess(APIException):
    code = 201
    msg = 'ok'
    error_code = 0


class APIDeleteSuccess(APIException):
    code = 202
    msg = 'delete ok'
    error_code = 1


class APIUpdateSuccess(APIException):
    code = 200
    msg = 'update ok'
    error_code = 2


class APIUpdateFail(APIException):
    code = 400
    msg = 'update fail'
    error_code = 2



class APIServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake!'
    error_code = 999


class APIParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class APINotFound(APIException):
    code = 404
    msg = 'the resource are not found'
    error_code = 1001


class APIAuthFailed(APIException):
    code = 401
    msg = 'authorization failed'
    error_code = 1005


class APIForbidden(APIException):
    code = 403
    error_code = 1004
    msg = 'forbidden, not in scope'
