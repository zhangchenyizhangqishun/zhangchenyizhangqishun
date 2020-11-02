#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on June 28, 2019
@author: hzhuangfg
'''
from smokeUtils import *
from com.util import gen_random_target
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式

def sendCaptchaForUpdatePhone(captcha,new_password,token):
    with pytest.allure.step("修改手机号发送验证码 captcha={0}，new_password={1}".format(captcha,new_password)):
        resp = hoolinkBaseTool.sendCaptchaForUpdatePhone(captcha,new_password,token)
        assert check_value(resp.checker, True)

def updatePassword(captcha,new_password,token):
    with pytest.allure.step("修改用户密码 captcha={0}，new_password={1}".format(captcha,new_password)):
        resp = hoolinkBaseTool.updatePassword(captcha,new_password,token)
        assert check_value(resp.checker, True)

def listPage(userName, customerNo, pageNo, pageSize, token):
    with pytest.allure.step("获取角色列表 userName={0}".format(userName)):
        resp = hoolinkBaseTool.listPage(customerNo, pageNo, pageSize, token)
        roleIds = [role.id for role in resp.data.list]
        assert check_value(resp.checker, True)
        return roleIds

def updateRoleStatus(roleId,status,token):
    with pytest.allure.step("更新角色状态 roleId={0}，status={1}".format(roleId,status)):
        resp = hoolinkBaseTool.updateRoleStatus(roleId, status, token)
        assert check_value(resp.checker, True)

def pageByParam(userName,pageNo, pageSize,token):
    with pytest.allure.step("获取用户列表 userName={0}".format(userName)):
        resp = hoolinkBaseTool.pageByParam(pageNo, pageSize, token ,fuzzyName='', fuzzyPhone='',fuzzyRole='',projectId='',status='')
        assert check_value(resp.checker, True)
        userIds = [user.id for user in resp.data.list]
        return userIds

def userPageByParam(userName,pageNo, pageSize,token, fuzzyName, fuzzyPhone,fuzzyRole,projectId,status):
    with pytest.allure.step("获取用户列表 userName={0}".format(userName)):
        resp = hoolinkBaseTool.pageByParam(pageNo, pageSize, token, fuzzyName, fuzzyPhone,fuzzyRole,projectId,status)
        assert check_value(resp.checker, True)
        return resp

def getForUpdate(userId, token):
    with pytest.allure.step("获取用户信息 userId={0}".format(userId)):
        resp = hoolinkBaseTool.getForUpdate(userId, token)
        assert check_value(resp.checker, True)
        return resp

def userLogin(account,password,customerNo,message):
    with pytest.allure.step("用户登录 account={0}， password = {1}， customerNo = {2}".format(account, password, customerNo)):
        resp = hoolinkBaseTool.login(account, password, customerNo)
        assert check_resp_msg(resp, message) is True
        return resp

def userLoginInRole(userId, roleStatus, token, password, message):
    resp = getForUpdate(userId, token)
    updateRoleStatus(resp.data.roleId, roleStatus, token)        # 禁用用户对应角色
    resetPassword(userId, token)
    updateStatus(userId, roleStatus, token, None)                # 更新用户状态
    userLogin(resp.data.account, password, resp.data.customerNo, message)

def listByCustomerNo(customerNo, token):
    with pytest.allure.step("获取角色列表 customerNo={0}".format(customerNo)):
        resp = hoolinkBaseTool.listByCustomerNo(customerNo, token)
        assert check_value(resp.checker, True)
        currencyMenuIds0 = [key for key in resp('$..*[@.menuType is %s].key' % 0)]
        # currencyMenuIds1 = [key for key in resp('$..*[@.menuType is %s].key' % 1)]
        # currencyMenuIds = currencyMenuIds0 + currencyMenuIds1
        return currencyMenuIds0

def createRole(customerNo,currencyMenuIds,token,readonly):
    name = 'roleName' + gen_random_target()
    description = 'roleDesc' + gen_random_target()
    with pytest.allure.step("创建角色 customerNo={0},currencyMenuIds={1}".format(customerNo,currencyMenuIds)):
        resp = hoolinkBaseTool.createRole(customerNo,currencyMenuIds,token,readonly,name,description)
        assert check_value(resp.checker, True)
        return resp.data

def getRoleById(roleId,token):
    with pytest.allure.step("获取角色详情 roleId={0}".format(roleId)):
        resp = hoolinkBaseTool.getRoleById(roleId,token)
        assert check_value(resp.checker, True)
        return resp.data

def createUser(roleId,sex,token):
    with pytest.allure.step("创建用户 roleId={0}".format(roleId)):
        name = account = 'tester_' + gen_random_target('port')
        resp = hoolinkBaseTool.createUser(account,roleId, name, sex,token)
        assert check_value(resp.checker, True)
        return resp.data ,account

def updateUserRole(userId, roleId, token):
    with pytest.allure.step("更改用户角色 userId={0}，roleId={1}".format(userId,roleId)):
        resp = hoolinkBaseTool.updateUserRole(userId, roleId, token)
        assert check_value(resp.checker, True)

def updateStatus(userId, status, token, message):
    with pytest.allure.step("启用、禁用用户 userId={0}，status={1}".format(userId,status)):
        resp = hoolinkBaseTool.updateStatus(userId, status, token)
        # assert check_value(resp.checker, True)
        assert check_value(resp.message, message)

def removeUser(userId, token):
    with pytest.allure.step("删除用户 userId={0}".format(userId)):
        resp = hoolinkBaseTool.removeUser(userId, token)
        assert check_value(resp.checker, True)

def resetPasswordForLogin(newPassword, token):
    with pytest.allure.step("新用户登录重置密码 newPassword={0}".format(newPassword)):
        resp = hoolinkBaseTool.resetPasswordForLogin(newPassword, token)
        assert check_value(resp.checker, True)

def resetPassword(userId, token):
    with pytest.allure.step("重置用户密码 userId={0}".format(userId)):
        resp = hoolinkBaseTool.resetPassword(userId, token)
        assert check_value(resp.checker, True)


def updateSex(userSex, token):
    with pytest.allure.step("更新用户性别 userSex={0}".format(userSex)):
        resp = hoolinkBaseTool.updateBaseSex(userSex, token)
        assert check_value(resp.checker, True)

def updateName(userName, token):
    with pytest.allure.step("更新用户姓名 userName={0}".format(userName)):
        resp = hoolinkBaseTool.updateBaseName(userName, token)
        assert check_value(resp.checker, True)

def getUserInfo(userName, token):
    with pytest.allure.step("获取用户信息 userName={0}".format(userName)):
        resp = hoolinkBaseTool.getUserInfo(token)
        assert check_value(resp.checker, True)
        return resp

def listProject(userName, pageNo, pageSize, token):
    with pytest.allure.step("查询项目列表 userName={0}".format(userName)):
        resp = hoolinkBaseTool.listProject(pageNo, pageSize, token)
        assert check_value(resp.checker, True)
        return resp

def getProjectById(projectId,token):
    with pytest.allure.step("项目详情查询 projectId={0}".format(projectId)):
        resp = hoolinkBaseTool.getProjectById(projectId,token)
        assert check_value(resp.checker, True)
        return resp

def readOwnerName(customerNo, ownerName, token):
    with pytest.allure.step("模糊查询用户名 customerNo={0}，ownerName={1}".format(customerNo,ownerName)):
        resp = hoolinkBaseTool.readOwnerName(customerNo, ownerName, token)
        assert check_value(resp.checker, True)
        # datas = [data for data in resp.data]
        names = [name for name in resp('$..*[@.phone is None].name')]
        return names

def updateOwnerName(projectId,ownerName,ownerPhone,token):
    with pytest.allure.step("修改项目责任人 projectId={0}，ownerName={1}，ownerPhone".format(projectId, ownerName, ownerPhone)):
        resp = hoolinkBaseTool.updateOwnerName(projectId, ownerName, ownerPhone, token)
        assert check_value(resp.checker, True)
        return resp

# @allure.severity("normal")
# @allure.feature(u"测试模块_用户管理")
# @allure.story(u"测试story_重绑用户手机号")
# def test_changeUserPhone(account='tester_net',password='888888',customerNo='netease',vcode='hoolink2019'):
#     """
#     修改手机号流程：用户登录，发送验证码，获取验证码，校验验证码，更新手机号
#     """
#     token = login(account, password, customerNo)('$.data.token')
#     with pytest.allure.step("修改手机号发送短信 token={0}".format(token)):
#         resp = hoolinkBasetool.sendCaptchaForUpdatePhone(token)
#         assert check_value(resp.checker, True)
#     with pytest.allure.step("修改手机号验证短信 token={0}".format(token)):
#         resp = hoolinkBasetool.checkCaptchaForUpdatePhone(vcode,token)
#         assert check_value(resp.checker, True)
#         phone = gen_random_target()
#     with pytest.allure.step("向重新绑定手机号发送短信 phone={0} ，vcode={1}".format(phone,vcode)):
#         resp = hoolinkBasetool.sendCaptchaForNewPhone(phone,vcode,token)
#         assert check_value(resp.checker, True)
#     with pytest.allure.step("更新手机号 vcode={0} ，phone={1}".format(vcode, phone)):
#         resp = hoolinkBasetool.updatePhone(vcode,vcode,phone,token)
#         assert check_value(resp.checker, True)


# @allure.severity("normal")
# @allure.feature(u"测试模块_用户管理")
# @allure.story(u"测试story_修改密码")
# def test_updatePassword(account='tester_net',password='888888',customerNo='netease'):
#     """
#     用户tester登录，角色初始化-创建角色roleA，创建项目A，根据角色A项目A创建用户testerA，用户testerA登录跳转至重置密码页面，修改密码，用户testerA绑定手机号流程
#     """
#     token = login(account, password, customerNo)('$.data.token')
#     new_password = '123456'
#     captcha = 'hoolink2019'
#     updatePassword(captcha,new_password,token)
#     userLogin(account, password, customerNo, None)

@allure.severity("normal")
@allure.feature(u"测试模块_用户管理")
@allure.story(u"测试story_修改姓名")
def test_updateName(account='huangfg',password='888888',customerNo='1001'):
    """
    用户tester登录，更新用户姓名，获取用户信息，校验更改之后姓名
    """
    token = login(account, password, customerNo)('$.data.token')
    userName = gen_random_target('email')
    updateName(userName,token)
    resp = getUserInfo(account, token)
    check_value(userName,resp.data.name)


@allure.severity("normal")
@allure.feature(u"测试模块_用户管理")
@allure.story(u"测试story_修改性别")
def test_updateSex(account='huangfg',password='888888',customerNo='1001'):
    """
    用户tester登录，获取用户性别，更新用户性别，再次获取用户性别，校验更改之后性别
    """
    token = login(account, password, customerNo)('$.data.token')
    resp = getUserInfo(account, token)
    userSex = True if resp.data.sexName == '女' else False
    updateSex(userSex,token)
    resp = getUserInfo(account, token)
    userSex_ = True if resp.data.sexName == '男' else False
    check_value(userSex,userSex_)


@allure.severity("normal")
@allure.feature(u"测试模块_项目管理")
@allure.story(u"测试story_修改项目责任人")
def test_updateOwnerName(account='huangfg',password='888888',customerNo='1001',ownerName='fuxiuxia'):
    """
    用户tester登录，获取项目列表，模糊查询用户名，如果匹配修改项目责任人，更新之后查询项目详情，校验项目责任人和手机号
    """
    token = login(account, password, customerNo)('$.data.token')
    resp = listProject(account, 1, 10, token)
    for project in resp.data.list:
        projectId = project.id
        names = readOwnerName(customerNo, ownerName, token)
        ownerPhone = gen_random_target('mobile')
        updateOwnerName(projectId,names[0],ownerPhone,token)
        resp = getProjectById(projectId, token)
        check_value(ownerName, resp.data.ownerName)
        check_value(ownerPhone, resp.data.ownerPhone)


# @allure.severity("normal")
# @allure.feature(u"测试模块_用户管理")
# @allure.story(u"测试story_查找用户")
# @pytest.mark.parametrize("account,password,menuList", [
#     ('huangfg', '888888', 1001,'','','',''),
#     ('test_huangfg', '123456', ['个人中心','基本信息','管理中心','用户管理']),
#     ('test_huangfg', '123456', ['管理中心','角色管理']),
#     ('test_huangfg', '123456', ['管理中心','项目管理']),
# ])
# def test_userPageByParam(userName,password,customerNo,fuzzyName,fuzzyPhone,fuzzyRole,projectId,status):
#     """
#     用户tester登录，获取角色列表，禁用角色，查询角色下用户列表，获取用户信息，用户testerA登录提示角色被禁用，查询用户禁用角色是否包含角色A，启用角色，用户testerA登录登录成功
#     """
#     token = login(userName, password, customerNo)('$.data.token')
#     # roleIds = listPage(userName,customerNo,pageNo,pageSize,token)
#     # for roleId in roleIds:
#     #     updateRoleStatus(roleId,False,token)
#     resp = userPageByParam(userName,1,10,token,fuzzyName, fuzzyPhone,fuzzyRole,projectId,status)



        # userLoginInRole(userId,roleIds,token,init_password,u'该账户所属角色已被禁用，请联系管理员')


@allure.severity("normal")
@allure.feature(u"测试模块_角色管理")
@allure.story(u"测试story_禁用启用角色")
def test_disableEnableRole(userName='huangfg',password='888888',customerNo='1001',pageNo=1, pageSize=10):
    """
    用户tester登录，获取角色列表，禁用角色，启用角色
    """
    token = login(userName, password, customerNo)('$.data.token')
    roleIds = listPage(userName, customerNo, pageNo, pageSize, token)
    for roleId in roleIds:
        updateRoleStatus(roleId, False, token)
        updateRoleStatus(roleId, True, token)


@allure.severity("normal")
@allure.feature(u"测试模块_角色管理")
@allure.story(u"测试story_禁用角色用户登录")
def test_disableRoleAndUserLogin(userName='huangfg',password='888888',customerNo='1001',init_password='123456',userId=991):
    """
    用户tester登录，获取用户列表，获取用户信息，禁用用户对应角色，用户testerA登录账户已被禁用，禁用用户对应角色，启用用户，用户testerA登录登录成功
    """
    token = login(userName, password, customerNo)('$.data.token')
    userLoginInRole(userId, False, token, init_password, u'账户已被禁用，请联系管理员')
    userLoginInRole(userId, True, token, init_password, None)

@allure.severity("normal")
@allure.feature(u"测试模块_用户管理")
@allure.story(u"测试story_禁用用户用户登录")
def test_disableUserAndUserLogin(userName='huangfg',password='888888',customerNo='1001',init_password='123456',roleId=172,userId=991):
    """
    用户tester登录，获取用户列表，查询用户详情，更改用户角色为禁用角色，重置密码，禁用用户A，用户testerA登录提示账户已被禁用，启用用户A失败提示角色被禁用，用户testerA登录登录失败
    1.角色被禁用，可以禁用用户
    2.角色被禁用，无法启用用户
    """
    token = login(userName, password, customerNo)('$.data.token')
    updateRoleStatus(roleId, False, token)
    # for userId in pageByParam(userName, pageNo, pageSize, token):
    updateUserRole(userId, roleId, token)                   # 更新用户角色：roleId=172 API测试角色禁用状态，userId=991
    resp = getForUpdate(userId, token)
    assert check_value(resp.data.status, False)             # 角色被禁用此时用户禁用状态
    resetPassword(userId, token)                            # 重置用户密码
    updateStatus(userId, False, token, None)                # 禁用用户 - 用户可以被重复禁用
    userLogin(resp.data.account, init_password, resp.data.customerNo, u'账户已被禁用，请联系管理员')
    updateStatus(userId, True, token, u'角色被禁用')        # 启用用户提示角色被禁用
    userLogin(resp.data.account, init_password, resp.data.customerNo, u'账户已被禁用，请联系管理员')


@allure.severity("normal")
@allure.feature(u"测试模块_用户管理")
@allure.story(u"测试story_创建用户")
def test_createRoleAndEdit(userName='huangfg',password='888888',customerNo='1001',init_password='123456',readonly=True,sex=True):
    """
    用户tester登录，获取角色列表，创建角色，获取角色详情，根据创建角色创建用户，禁用用户，用户testerA登录提示账户已被禁用，启用用户，用户testerA登录登录成功，删除用户，用户testerA登录登录提示登录账号或密码不正确
    """
    token = login(userName, password,customerNo)('$.data.token')
    currencyMenuIds = listByCustomerNo(customerNo,token)
    roleId = createRole(customerNo, currencyMenuIds, token, readonly)
    getRoleById(roleId,token)
    userId,account = createUser(roleId,sex,token)
    updateStatus(userId, False, token, None)
    userLogin(account, init_password,customerNo, u'账户已被禁用，请联系管理员')
    updateStatus(userId, True, token, None)
    resp = userLogin(account, init_password, customerNo, None)
    assert check_value(resp.data.resetPassword,True)                        #新用户登录重置密码
    tokenA = resp('$.data.token')
    resetPasswordForLogin(password, tokenA)
    resp = userLogin(account, password, customerNo, None)
    assert check_value(resp.data.resetPassword, False)
    removeUser(userId, token)
    userLogin(account, init_password, customerNo, u'登录账号或密码不正确') #当用户被删除时，返回登录账号或密码不正确




