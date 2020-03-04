import json
from tornado.web import RequestHandler
from library.Result import Result


# 错误定义类
class NotFoundHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.set_status(404)
        self.write(json.dumps(Result(code=404, msg="请求页面不存在!").json()))
