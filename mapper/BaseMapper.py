#!/usr/bin/env python
from library.Decorate import DI
from library.Overall import Overall


@DI(overall=Overall.getInstance())
class BaseMapper():
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def conf(self):
        return self.overall.conf

    @property
    def utils(self):
        return self.overall.utils

    @property
    def redis(self):
        return self.overall.redis

    @property
    def session(self):
        return self.overall.session

    @property
    def jolly_session(self):
        return self.overall.jolly_session


    def save(self, obj):
        """ 保存对象，支持批量写入"""
        if isinstance(obj, list):
            res = self.session.add_all(obj)
        else:
            res = self.session.add(obj)
        self.session.flush()
        return res

