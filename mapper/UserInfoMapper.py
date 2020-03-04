#!/usr/bin/env python

from sqlalchemy import desc, or_
from datetime import datetime
from .BaseMapper import BaseMapper
from models.UserInfo import UserInfo


class UserInfoMapper(BaseMapper):

    # 获取所有用户信息
    def getUserList(self):
        userList = self.session.query(UserInfo.user_id, UserInfo.group_id, UserInfo.user_name, UserInfo.phone, UserInfo.email,
                                      UserInfo.state, UserInfo.create_date, UserInfo.modify_date).all()
        return userList

    # 获取指定用户信息
    def getUserInfo(self, userId):
        userInfo = self.session.query(UserInfo.user_id, UserInfo.group_id, UserInfo.user_name, UserInfo.phone, UserInfo.email,
                                      UserInfo.state, UserInfo.create_date, UserInfo.modify_date).filter(UserInfo.user_id==userId).first()
        return userInfo

    # 使用登录名查询用户信息
    def getUserInfoByLoginName(self, loginName):
        userInfo = self.session.query(UserInfo).filter(or_(UserInfo.phone==loginName, UserInfo.email==loginName)).first()
        return userInfo

    # 更新用户token
    def updTokenByUserId(self, userId, token=None):
        modifyDate = datetime.now()
        params = {'modify_date': modifyDate, 'token': token}
        userInfo = self.session.query(UserInfo).filter(UserInfo.user_id == userId).update(params)
        return userInfo

    # 添加用户
    def addUserInfo(self, userName, password, phone, email):
        userInfo = UserInfo()
        userInfo.user_name = userName
        userInfo.password = password
        userInfo.phone = phone
        userInfo.email = email
        return self.session.add(userInfo)

    # 根据手机号码与邮箱查找用户
    def getUserInfoByPhoneOrEmail(self, phone=None, email=None):
        if phone:
            userInfo = self.session.query(UserInfo.user_id).filter(UserInfo.phone == phone).first()
            if userInfo:
                return "手机号码已存在"
        if email:
            userInfo = self.session.query(UserInfo.user_id).filter(UserInfo.email == email).first()
            if userInfo:
                return "邮箱地址已存在"
        return None

    # 更新用户信息
    def updUserInfoByUserId(self,userId, groupId=None, userName=None, password=None, phone=None, email=None):
        userInfo = self.session.query(UserInfo).filter(UserInfo.user_id == userId)
        param = {}
        if groupId:
            param['group_id'] = groupId
        if userName:
            param['user_name'] = userName
        if password:
            param['password'] = password
        if phone:
            param['phone'] = phone
        if email:
            param['email'] = email
        param['modify_date'] = datetime.now()
        return userInfo.update(param)