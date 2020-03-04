import uuid, re
from .BaseService import BaseService
from mapper.UserInfoMapper import UserInfoMapper
from library.Exception import UserException
from library.Decorate import Transaction
from library.Result import Result


class UserInfoService(BaseService):
    def __init__(self):
        self.userInfoMapper = UserInfoMapper.getInstance()
        super().__init__()

    # 用户登录验证与Token设置
    @Transaction(name="session")
    def userLogin(self, loginName, password):
        userInfo  = self.userInfoMapper.getUserInfoByLoginName(loginName)
        if userInfo is None:
            raise UserException(code=11002)
        if userInfo.state == '2':
            raise UserException(code=11000)
        if userInfo.password == self.utils.md5(password):
            token = str(uuid.uuid1())
            userId = self.userInfoMapper.updTokenByUserId(userId=userInfo.user_id, token=token)
            self.redis.setex(token, 24 * 60 * 60, {'userId': userId})
            return Result(data={'token': token, 'userName': userInfo.user_name}, msg='登录成功')
        else:
            raise UserException(code=11001)

    # 注销登录
    @Transaction(name="session")
    def logout(self, userId, token):
        if self.redis.delete(token):
            self.userInfoMapper.updTokenByUserId(userId, token=None)
            return Result(msg='退出成功')
        else:
            raise UserException(code=11003)

    # 获取所有用户信息
    def getUserList(self):
        userList = self.userInfoMapper.getUserList()
        return userList

    # 查询指定用户信息
    def getUserInfo(self, userId):
        userInfo = self.userInfoMapper.getUserInfo(userId)
        return userInfo

    # 使用token获取redis中保存得用户Id
    def getUserIdByTonken(self, token):
        return self.redis.get(token)

    # 添加新用户
    @Transaction(name="session")
    def addUserInfo(self, userName, password, phone, email):
        message = self.userInfoMapper.getUserInfoByPhoneOrEmail(phone=phone, email=email)
        if message:
            raise UserException(code=11011, desc=message)
        if phone.isdigit() is False or len(phone) != 11:
            raise UserException(code=11007)
        if re.match(r'^([\w]+\.*)([\w]+)\@[\w]+\.\w{3}(\.\w{2}|)$', email) is None:
            raise UserException(code=11008)
        self.userInfoMapper.addUserInfo(userName, self.utils.md5(password), phone, email)
        return Result(msg='用户添加完成')

    # 更新用户信息
    @Transaction(name='session')
    def updUserInfoByUserId(self, userId, groupId=None, userName=None, password=None, phone=None, email=None):
        if password:
            password = self.utils.md5(password)
        if phone or email:
            userInfo = self.userInfoMapper.getUserInfo(userId)
            if phone != userInfo.phone or email != userInfo.email:
                msg = self.userInfoMapper.getUserInfoByPhoneOrEmail(phone=phone, email=email)
                if msg is not None:
                    return Result(code=300, msg=msg)
        self.userInfoMapper.updUserInfoByUserId(userId, groupId=groupId, userName=userName, password=password, phone=phone, email=email)
        return Result(msg='更新完成')