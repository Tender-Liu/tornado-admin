#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from oslo_context import context
from tornado.web import RequestHandler
from library.Exception import CustomException
from library.Overall import Overall
from library.Result import Result
from library.Utils import Utils
from service.UserInfoService import UserInfoService


class BaseHandler(RequestHandler):
    uid = None
    token = None

    def __init__(self, application, request, **kwargs):
        context.RequestContext()
        self.post_arguments = {}
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def compute_etag(self):
        """ 取消缓存 """
        return None

    def prepare(self):
        if self.request.method == 'OPTIONS':
            return self.options()

        # 非登录接口Token验证
        if self.request.path not in ["/api/user/login"]:
            token = self.request.headers.get("X-Token", None)
            try:
                assert token is not None
                data = UserInfoService().getUserIdByTonken(token)
                if data is not None:
                    #: 后期权限扩展处 :#
                    self.userId = data['userId']
                    self.token = token
                else:
                    raise CustomException(code=1001)
            except AssertionError as e:
                raise CustomException(code=1002)

        try:
            if self.request.body:
                self.post_arguments = json.loads(self.request.body.decode('utf-8'))
        except Exception as ex:
            return self.json(Result(code=300, msg=str(ex)))

    def write_error(self, status_code, **kwargs):
        if isinstance(kwargs.get('exc_info')[1], CustomException):
            ce = kwargs.get('exc_info')[1]
            self.set_status(200)
            return self.json(Result(code=ce.code, msg=ce.msg))
        else:
            return self.json(Result(code=status_code, msg="未知错误"))

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers",
                        "X-Token, Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')

    def on_finish(self):
        """ 清理资源 """
        Overall.getInstance().clear()

    def json(self, result):
        self.write(json.dumps(result.json(), cls=Utils.JSONEncoder(), sort_keys=False))
        self.finish()

    def options(self, *args, **kwargs):
        self.set_status(204)
