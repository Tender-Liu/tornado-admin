from sqlalchemy.orm import scoped_session
from models import UnitymobSession
from config import conf
from library.MyRedis import MyRedis
from library.Utils import Utils
from tornado.ioloop import IOLoop


# 公共组件
class Overall(object):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.conf = conf
        self.utils = Utils
        self._session = None

    @property
    def currentIOloopInstance(self):
        return IOLoop.current()

    @property
    def session(self):
        """数据连接创建"""
        if self._session is None:
            self._session = scoped_session(UnitymobSession)
        return self._session

    @property
    def redis(self):
        return MyRedis.getInstance(host=conf.redis.host, port=conf.redis.port, db=conf.redis.db,
                                   password=conf.redis.password, decode_responses=False)

    def clear(self):
        """ 数据库 释放资源 """
        if self._session is not None:
            self._session.remove()
        self._session = None
