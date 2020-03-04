from library.Overall import Overall
from library.Decorate import DI


@DI(overall=Overall.getInstance())
class BaseService(object):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def session(self):
        return self.overall.session

    @property
    def redis(self):
        return self.overall.redis

    @property
    def utils(self):
        return self.overall.utils


    @property
    def conf(self):
        return self.overall.conf
