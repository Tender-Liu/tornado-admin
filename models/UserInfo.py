#!/usr/bin/env python

from .BaseModel import Base
from sqlalchemy import Column
from sqlalchemy.types import *
from datetime import datetime


class UserInfo(Base):
    __tablename__ = 'user_info'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, nullable=True)
    user_name = Column(String(50), nullable=False)
    password = Column(String(120), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    state = Column(Integer, nullable=False, default=1)
    token = Column(String(50), nullable=True)
    create_date = Column(DateTime, default=datetime.now())
    modify_date = Column(DateTime, default=datetime.now())


