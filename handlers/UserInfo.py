#!/usr/bin/env python

from library.Handlers import BaseHandler
from library.Result import Result
from library.Decorate import Return
from library.Route import route
from service.UserInfoService import UserInfoService


# 登录验证
@route(r"/user/login")
class UserLoginHandler(BaseHandler):
    @Return
    def post(self, *args, **kwargs):
        loginName = self.post_arguments.get('loginName', None)
        password = self.post_arguments.get('passWord', None)
        if loginName is None or password is None:
            return Result(code=300, msg='账号与密码都不能为空')
        return UserInfoService().userLogin(loginName, password)


# 登录注销
@route(r"/user/logout")
class UserLogoutHandler(BaseHandler):
    @Return
    def post(self, *args, **kwargs):
        return UserInfoService().logout(self.userId, self.token)


# 用户信息增删该查
@route(r"/user/info")
class UserListHandler(BaseHandler):
    @Return
    # 添加用户
    def post(self, *args, **kwargs):
        userName = self.post_arguments.get('userName', None)
        password = self.post_arguments.get('password', None)
        phone = self.post_arguments.get('phone', None)
        email = self.post_arguments.get('email', None)
        if userName and password and phone and email:
            return UserInfoService().addUserInfo(userName, password, phone, email)
        else:
            return Result(code=300, msg='账号与密码都不能为空')

    # 查询用户信息
    @Return
    def get(self, *args, **kwargs):
        return UserInfoService().getUserInfo(self.userId)

    # 删除用户
    @Return
    def delete(self, *args, **kwargs):
        return UserInfoService().getUserInfo(self.userId)

    # 更新用户信息，包含修改密码
    @Return
    def put(self, *args, **kwargs):
        groupId = self.post_arguments.get('groupId', None)
        userName = self.post_arguments.get('userName', None)
        password = self.post_arguments.get('password', None)
        phone = self.post_arguments.get('phone', None)
        email = self.post_arguments.get('email', None)
        if groupId or userName or password or phone or email:
            return UserInfoService().updUserInfoByUserId(self.userId, groupId=groupId,
                                                         userName=userName, password=password, phone=phone, email=email)
        else:
            return Result(code=300, msg='没有需要更新得数据')
