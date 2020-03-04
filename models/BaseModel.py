from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import as_declarative

Base = declarative_base()
# 所有数据公共对象

@as_declarative()
class Base(object):

    __table_args__ = {
        'mysql_charset': 'utf8mb4'
    }


    @property
    def columns(self):
        return [c.name for c in self.__table__.columns]

    @property
    def columnitems(self):
        return dict([(c, getattr(self, c)) for c in self.columns])

    @property
    def dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.columnitems)

    def tojson(self):
        return self.columnitems
