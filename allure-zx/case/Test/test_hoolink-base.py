#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on June 14, 2019
@author: hzhuangfg
'''
from testUtils import *
from com.util import load_csv_file
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式

# def check_resp_msg(resp,expectedMessage):
#     with pytest.allure.step("测试结果校验：{0} == {1}，{2} == {3}".format(resp.message, expectedMessage,resp.status,resp.checker)):
#         return True if resp.message == expectedMessage and resp.status == resp.checker else False


def check_resp_msg(resp,expectedMessage):
    with pytest.allure.step("测试结果校验：{0} == {1}".format(resp.message, expectedMessage)):
        return True if (resp.message == expectedMessage or resp.message.find(expectedMessage) != -1) else False

def get_dataProvider(caseDataFileName):
    caseDataDir = r'dataProvider\hoolink-base'
    currentDir=os.path.normpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
    dataProvider_path=os.path.join(currentDir, caseDataDir,caseDataFileName)
    return dataProvider_path

def checkUserStatus(resp, status):
    if status != '':                        #非空代表传了status字段
        statusList = [status for status in resp('$..*[@].status')]
        for status_ in statusList[1::]:     # 去掉第一个status是接口返回状态，并非用户状态
            assert check_value(status,status_)

def checkUserFuzzyName(resp,fuzzyName):
    if fuzzyName:
        # nameList = [name for name in resp('$..*[@].name')]
        # for name in nameList:
        for name in resp('$..*[@].name'):
            assert check_value_include(name,fuzzyName)

def checkUserFuzzyRole(resp,fuzzyRole):
    if fuzzyRole:
        for roleName in resp('$..*[@].roleName'):
            assert check_value_include(roleName, fuzzyRole)

def userPageByParam(userName,pageNo, pageSize,token, fuzzyName, fuzzyPhone,fuzzyRole,projectId,status):
    with pytest.allure.step("获取用户列表 userName={0}".format(userName)):
        resp = hoolinkBaseTool.pageByParam(pageNo, pageSize, token, fuzzyName, fuzzyPhone,fuzzyRole,projectId,status)
        assert check_value(resp.checker, True)
        return resp
test_data,ids = load_csv_file(get_dataProvider('listUser.csv'))
@allure.severity("normal")
@allure.feature(u"测试模块_用户管理")
@allure.story(u"测试story_查找用户")
@pytest.mark.parametrize("account,password,customerNo,fuzzyName,fuzzyPhone,fuzzyRole,projectId,status,expectedMessage",test_data,ids=ids,)
def test_getUserList(account,password,customerNo,fuzzyName,fuzzyPhone,fuzzyRole,projectId,status,expectedMessage):
    """
    用例描述：根据条件查找用户
    """
    token = login(account, password, customerNo)('$.data.token')
    resp = userPageByParam(account, 1, 10, token, fuzzyName, fuzzyPhone, fuzzyRole, projectId, status)
    checkUserStatus(resp, status)
    checkUserFuzzyName(resp, fuzzyName)
    checkUserFuzzyRole(resp, fuzzyRole)


def createUser(userAccount,roleId,userName,sex,token):
    userAccount = 'tester_'+gen_random_target() if userAccount.lower() == 'random' else userAccount
    userName = 'UA_' + gen_random_target() if userName.lower() == 'random' else userName
    with pytest.allure.step("创建用户 roleId={0}，account={1}，name={2}".format(roleId,userAccount,userName)):
        return hoolinkBaseTool.createUser(userAccount,roleId, userName, sex,token)
test_data,ids = load_csv_file(get_dataProvider('createUser.csv'))
@allure.severity("normal")
@allure.feature(u"测试模块_用户管理")
@allure.story(u"测试story_创建用户")
@pytest.mark.parametrize("account,password,customerNo,roleId,sex,userAccount,userName,expectedMessage",test_data,ids=ids,)
def test_createUser(account,password,customerNo,roleId,sex,userAccount,userName,expectedMessage):
    """
    用例描述：创建用户
    """
    token = login(account, password, customerNo)('$.data.token')
    resp = createUser(userAccount,roleId,userName,sex,token)
    assert check_resp_msg(resp,expectedMessage)

def updateUserStatus(userId, status, token):
    with pytest.allure.step("启用、禁用用户 userId={0}，status={1}".format(userId,status)):
        return hoolinkBaseTool.updateStatus(userId, status, token)
test_data,ids = load_csv_file(get_dataProvider('updateUserStatus.csv'))
@allure.severity("normal")
@allure.feature(u"测试模块_用户管理")
@allure.story(u"测试story_启用禁用用户")
@pytest.mark.parametrize("account,password,customerNo,userId,status,expectedMessage",test_data,ids=ids,)
def test_updateUserStatus(account,password,customerNo,userId,status,expectedMessage):
    """
    用例描述：启用、禁用用户
    """
    token = login(account, password, customerNo)('$.data.token')
    resp = updateUserStatus(userId, status, token)
    assert check_resp_msg(resp, expectedMessage)

def removeUser(userId, token):
    with pytest.allure.step("删除用户 userId={0}".format(userId)):
        return hoolinkBaseTool.removeUser(userId, token)
test_data,ids = load_csv_file(get_dataProvider('removeUser.csv'))
@allure.severity("normal")
@allure.feature(u"测试模块_用户管理")
@allure.story(u"测试story_删除用户")
@pytest.mark.parametrize("account,password,customerNo,userId,expectedMessage",test_data,ids=ids,)
def test_removeUser(account,password,customerNo,userId,expectedMessage):
    """
    用例描述：删除用户
    """
    token = login(account, password, customerNo)('$.data.token')
    resp = removeUser(userId, token)
    assert check_resp_msg(resp, expectedMessage)

def updateUserName(userName, token):
    with pytest.allure.step("更新用户姓名 userName={0}".format(userName)):
        return hoolinkBaseTool.updateBaseName(userName, token)
test_data,ids = load_csv_file(get_dataProvider('updateUserName.csv'))
@allure.severity("normal")
@allure.feature(u"测试模块_用户管理")
@allure.story(u"测试story_更新用户姓名")
@pytest.mark.parametrize("account,password,customerNo,userName,expectedMessage",test_data,ids=ids,)
def test_updateUserName(account,password,customerNo,userName,expectedMessage):
    """
    用例描述：更新用户姓名
    """
    token = login(account, password, customerNo)('$.data.token')
    resp = updateUserName(userName, token)
    assert check_resp_msg(resp, expectedMessage)

def updateUserSex(userSex, token):
    with pytest.allure.step("更新用户性别 userSex={0}".format(userSex)):
        return hoolinkBaseTool.updateBaseSex(userSex, token)
test_data,ids = load_csv_file(get_dataProvider('updateUserSex.csv'))
@allure.severity("normal")
@allure.feature(u"测试模块_用户管理")
@allure.story(u"测试story_更新用户性别")
@pytest.mark.parametrize("account,password,customerNo,userSex,expectedMessage",test_data,ids=ids,)
def test_updateUserSex(account,password,customerNo,userSex,expectedMessage):
    """
    用例描述：更新用户性别
    """
    token = login(account, password, customerNo)('$.data.token')
    resp = updateUserSex(userSex, token)
    assert check_resp_msg(resp, expectedMessage)


def readOwnerName(customerNo, ownerName, token):
    with pytest.allure.step("模糊查询用户名 customerNo={0}，ownerName={1}".format(customerNo,ownerName)):
        return hoolinkBaseTool.readOwnerName(customerNo, ownerName, token)
test_data,ids = load_csv_file(get_dataProvider('readOwnerName.csv'))
@allure.severity("normal")
@allure.feature(u"测试模块_用户管理")
@allure.story(u"测试story_用户名模糊查询")
@pytest.mark.parametrize("account,password,customerNo,ownerName,expectedMessage",test_data,ids=ids,)
def test_readOwnerName(account,password,customerNo,ownerName,expectedMessage):
    """
    用例描述：用户名模糊查询
    """
    token = login(account, password, customerNo)('$.data.token')
    resp = readOwnerName(customerNo, ownerName, token)
    assert check_resp_msg(resp, expectedMessage)
    for name in resp('$..name'):
        check_value_include(name,ownerName)

def updateOwnerName(projectId,ownerName,ownerPhone,token):
    ownerName = 'ON_' + gen_random_target() if ownerName.lower()=='random' else ownerName
    ownerPhone = gen_random_target('mobile') if ownerPhone.lower() == 'random' else ownerPhone
    with pytest.allure.step("修改项目责任人 projectId={0}，ownerName={1}，ownerPhone".format(projectId,ownerName,ownerPhone)):
        return hoolinkBaseTool.updateOwnerName(projectId,ownerName,ownerPhone,token)
test_data,ids = load_csv_file(get_dataProvider('updateOwnerName.csv'))
@allure.severity("normal")
@allure.feature(u"测试模块_用户管理")
@allure.story(u"测试story_修改项目责任人")
@pytest.mark.parametrize("account,password,customerNo,projectId,ownerName,ownerPhone,expectedMessage",test_data,ids=ids,)
def test_updateOwnerName(account,password,customerNo,projectId,ownerName,ownerPhone,expectedMessage):
    """
    用例描述：修改项目责任人
    """
    token = login(account, password, customerNo)('$.data.token')
    resp = updateOwnerName(projectId,ownerName,ownerPhone,token)
    assert check_resp_msg(resp, expectedMessage)

def createRole(customerNo,currencyMenuIds,token,readonly,name,description):
    # currencyMenuIds = eval(currencyMenuIds)
    name = 'roleName' + gen_random_target() if name.lower()=='random' else name
    description = 'roleDesc' + gen_random_target() if description=='random' else description
    with pytest.allure.step("创建角色 customerNo={0},currencyMenuIds={1}".format(customerNo,currencyMenuIds)):
        return hoolinkBaseTool.createRole(customerNo,currencyMenuIds,token,readonly,name,description)
test_data,ids = load_csv_file(get_dataProvider('createRole.csv'))
@allure.severity("normal")
@allure.feature(u"测试模块_角色管理")
@allure.story(u"测试story_创建角色")
@pytest.mark.parametrize("account,password,customerNo,currencyMenuIds,readonly,name,description,expectedMessage",test_data,ids=ids,)
def test_createRole(account,password,customerNo,currencyMenuIds,readonly,name,description,expectedMessage):
    """
    用例描述：创建角色
    """
    token = login(account, password, customerNo)('$.data.token')
    resp = createRole(customerNo,currencyMenuIds,token,readonly,name,description)
    assert check_resp_msg(resp, expectedMessage)

def updateRole(roleId,customerNo,name,description,currencyMenuIds,token,readonly):
    # currencyMenuIds = eval(currencyMenuIds)
    name = 'roleName' + gen_random_target() if name.lower() == 'random' else name
    description = 'roleDesc' + gen_random_target() if description == 'random' else description
    with pytest.allure.step("更新角色 customerNo={0}，roleId={1}，currencyMenuIds={2}".format(customerNo, roleId, currencyMenuIds)):
        return hoolinkBaseTool.updateRole(roleId,customerNo,name,description,currencyMenuIds,token,readonly)
test_data,ids = load_csv_file(get_dataProvider('updateRole.csv'))
@allure.severity("normal")
@allure.feature(u"测试模块_角色管理")
@allure.story(u"测试story_更新角色")
@pytest.mark.parametrize("account,password,customerNo,roleId,currencyMenuIds,readonly,name,description,expectedMessage",test_data,ids=ids,)
def test_updateRole(account,password,customerNo,roleId,currencyMenuIds,readonly,name,description,expectedMessage):
    """
    用例描述：更新角色
    """
    token = login(account, password, customerNo)('$.data.token')
    resp = updateRole(roleId,customerNo,name,description,currencyMenuIds,token,readonly)
    assert check_resp_msg(resp, expectedMessage)
def updateRoleStatus(roleId,status,token):
    with pytest.allure.step("更新角色状态 roleId={0}，status={1}".format(roleId,status)):
        return hoolinkBaseTool.updateRoleStatus(roleId, status, token)
test_data,ids = load_csv_file(get_dataProvider('updateRoleStatus.csv'))
@allure.severity("normal")
@allure.feature(u"测试模块_角色管理")
@allure.story(u"测试story_修改角色状态")
@pytest.mark.parametrize("account,password,customerNo,roleId,status,expectedMessage",test_data,ids=ids,)
def test_updateRoleStatus(account,password,customerNo,roleId,status,expectedMessage):
    """
    用例描述：更新角色状态
    """
    token = login(account, password, customerNo)('$.data.token')
    resp = updateRoleStatus(roleId,status,token)
    assert check_resp_msg(resp, expectedMessage)
