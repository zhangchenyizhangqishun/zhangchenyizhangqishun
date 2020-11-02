#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on June 17, 2019
@author: hzhuangfg
'''
from imp import reload

import pytest
from testUtils import *
from com.util import load_csv_file
import sys, os

reload(sys)
sys.setdefaultencoding('utf-8')  # 修改默认的编码模式


def check_resp_msg_include(resp, expectedMessage):
    with pytest.allure.step("测试结果校验：{0} == {1}".format(resp.message, expectedMessage)):
        return True if (resp.message == expectedMessage or resp.message.find(expectedMessage) != -1) else False


def check_resp_msg(resp, expectedMessage):
    with pytest.allure.step("测试结果校验：{0} == {1}".format(resp.message, expectedMessage)):
        return True if resp.message == expectedMessage else False


def get_dataProvider(caseDataFileName):
    caseDataDir = r'dataProvider\manage-base'
    currentDir = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    dataProvider_path = os.path.join(currentDir, caseDataDir, caseDataFileName)
    return dataProvider_path


def getCurrentRoleMenu(menuList, permissionFlag, token):
    with pytest.allure.step("获取用户角色菜单按钮 menuList={0}".format(menuList)):
        resp = manageBaseTool.getCurrentRoleMenu(token)
        assert check_value(resp.checker, True)
        parentMenuIdList = []
        childrenMenuIdList = []
        for value in menuList:
            parentMenuIds = [key for key in resp('$..*[@.title is "%s" and len(@.children) > 0 ].key' % value)]
            parentMenuIdList += parentMenuIds
            childrenMenuIds = [key for key in resp('$..*[@.title is "%s" and len(@.children) < 1 ].key' % value)]
            childrenMenuIdList += childrenMenuIds
        parentRoleMenuVOList = [{'menuId': menuId, 'permissionFlag': None} for menuId in parentMenuIdList]
        childrenRoleMenuVOList = [{'menuId': menuId, 'permissionFlag': permissionFlag} for menuId in childrenMenuIdList]
        RoleMenuVOList = parentRoleMenuVOList + childrenRoleMenuVOList
        return RoleMenuVOList


def createRole(roleName, roleDesc, roleType, roleMenuVOList, token):
    roleName = 'RN' + gen_random_target() if roleName.lower() == 'random' else roleName
    roleDesc = 'RD' + gen_random_target() if roleDesc == 'random' else roleDesc
    with pytest.allure.step(
            "创建角色 roleName={0}，roleDesc={1}，roleMenuVOList={2}".format(roleName, roleDesc, roleMenuVOList)):
        return manageBaseTool.createRole(roleName, roleType, roleMenuVOList, roleDesc, token)


test_data, ids = load_csv_file(get_dataProvider('createRole.csv'))


@allure.severity("normal")
@allure.feature(u"管理平台_角色管理")
@allure.story(u"测试story_创建角色")
@pytest.mark.parametrize("account,password, roleName, roleDesc, roleType, menuList, permissionFlag, expectedMessage",
                         test_data, ids=ids, )
def test_createRole(account, password, roleName, roleDesc, roleType, menuList, permissionFlag, expectedMessage):
    """
    用例描述：创建角色
    """
    token = manageLogin(account, password)('$.data.token')
    roleMenuVOList = getCurrentRoleMenu(menuList, permissionFlag, token)
    resp = createRole(roleName, roleDesc, roleType, roleMenuVOList, token)
    assert check_resp_msg(resp, expectedMessage)
    # checkListWarrantyList(resp, companyName, projectName)


def updateMangeRoleStatus(roleId, roleStatus, token):
    with pytest.allure.step("禁用、启用角色 roleId={0},roleStatus={1}".format(roleId, roleStatus)):
        return manageBaseTool.updateRoleStatus(roleId, roleStatus, token)


test_data, ids = load_csv_file(get_dataProvider('updateRoleStatus.csv'))


@allure.severity("normal")
@allure.feature(u"管理平台_用户管理")
@allure.story(u"测试story_启用禁用用户")
@pytest.mark.parametrize("account,password,roleId,roleStatus,expectedMessage", test_data, ids=ids, )
def test_updateMangeRoleStatus(account, password, roleId, roleStatus, expectedMessage):
    """
    用例描述：启用禁用角色
    """
    token = manageLogin(account, password)('$.data.token')
    resp = updateMangeRoleStatus(roleId, roleStatus, token)
    assert check_resp_msg(resp, expectedMessage)


def updateRole(roleId, roleName, roleMenuVOList, roleDesc, roleType, token):
    roleName = 'UPRN' + gen_random_target() if roleName.lower() == 'random' else roleName
    roleDesc = 'UPRD' + gen_random_target() if roleDesc == 'random' else roleDesc
    with pytest.allure.step(
            "更新角色 roleId={0}，roleName={1}，roleMenuVOList={2}，roleDesc={3}，roleType={4}".format(roleId, roleName,
                                                                                               roleMenuVOList, roleDesc,
                                                                                               roleType)):
        return manageBaseTool.updateRole(roleId, roleName, roleMenuVOList, roleDesc, roleType, token)


test_data, ids = load_csv_file(get_dataProvider('updateRole.csv'))


@allure.severity("normal")
@allure.feature(u"管理平台_角色管理")
@allure.story(u"测试story_更新角色")
@pytest.mark.parametrize(
    "account,password, roleId, roleName, roleDesc, roleType, menuList, permissionFlag, expectedMessage", test_data,
    ids=ids, )
def test_updateRole(account, password, roleId, roleName, roleDesc, roleType, menuList, permissionFlag, expectedMessage):
    """
    用例描述：更新角色
    """
    token = manageLogin(account, password)('$.data.token')
    roleMenuVOList = getCurrentRoleMenu(menuList, permissionFlag, token)
    resp = updateRole(roleId, roleName, roleMenuVOList, roleDesc, roleType, token)
    assert check_resp_msg(resp, expectedMessage)


def checkSearchValueInclude(resp, searchValue, key):
    for value in resp('$..*[@].%s' % key):
        assert check_value_include(value, searchValue)


def checkSearchValue(resp, searchValue, key):
    if searchValue:
        for value in resp('$..*[@].%s' % key):
            assert check_value(value, searchValue)


def checkListIncludeList(resp, searchValue, key):
    if searchValue:
        for value in resp('$..*[@].%s' % key):
            assert check_list_include_list(value, searchValue)


def listRoleByPage(status, searchValue, token):
    with pytest.allure.step("获取角色列表 status={0}，searchValue={1}".format(status, searchValue)):
        resp = manageBaseTool.listRoleByPage(1, 10, token, status, searchValue)
        return resp


test_data, ids = load_csv_file(get_dataProvider('listRoleByPage.csv'))


@allure.severity("normal")
@allure.feature(u"管理平台_用户管理")
@allure.story(u"测试story_查询角色列表")
@pytest.mark.parametrize("account,password,status,roleName,expectedMessage", test_data, ids=ids, )
def test_listRoleByPage(account, password, status, roleName, expectedMessage):
    """
    获取角色列表
    """
    token = manageLogin(account, password)('$.data.token')
    resp = listRoleByPage(status, roleName, token)
    assert check_resp_msg(resp, expectedMessage)
    checkSearchValueInclude(resp, roleName, 'roleName')
    checkSearchValue(resp, status, 'roleStatus')


def listUserByPage(token, status, roleId, groupParam, deptId):
    with pytest.allure.step(
            "获取用户列表 status={0}，roleId={1}，groupParam={2}，deptId={3}".format(status, roleId, groupParam, deptId)):
        resp = manageBaseTool.listUserByPage(1, 10, token, status, roleId, groupParam, deptId)
        return resp


def getDeptTree(labelList, token):
    with pytest.allure.step("获取组织架构树 token={0}".format(token)):
        resp = manageBaseTool.getDeptTree(token)
        deptIds = []
        for label in labelList:
            deptId = [key for key in resp('$..*[@.label is "%s"].value' % label)]  # 将生成器转换成列表，方便两个列表相加
            deptIds += deptId  # [1,2] + [3,4] --> [1,2,3,4]
        return deptIds


def getDictInfo(key, roleName, token):
    with pytest.allure.step("获取基础字典值数据 key={0}".format(key)):
        resp = manageBaseTool.getDictInfo(key, token)
        key = resp('$..*[@.value is "%s"].key' % roleName)
        return next(key) if roleName else ''


test_data, ids = load_csv_file(get_dataProvider('listUserByPage.csv'))


@allure.severity("normal")
@allure.feature(u"管理平台_用户管理")
@allure.story(u"测试story_查询角色列表")
@pytest.mark.parametrize("account,password,labelList,roleName,status,groupParam,expectedMessage", test_data, ids=ids, )
def test_listUserByPage(account, password, labelList, roleName, status, groupParam, expectedMessage):
    """
    获取用户列表
    """
    token = manageLogin(account, password)('$.data.token')
    deptIds = getDeptTree(labelList, token)
    roleId = getDictInfo('role', roleName, token)
    resp = listUserByPage(token, status, roleId, groupParam, deptIds)
    # checkListIncludeList(resp, labelList, 'deptNameList')
    checkSearchValue(resp, status, 'status')
    checkSearchValue(resp, roleName, 'roleName')
    checkSearchValueInclude(resp, groupParam, 'name')


def createUser(userAccount, userName, userNo, sex, roleId, encryLevelCompany, position, deptIdList, encryLevelDept,
               token, imgId):
    userAccount = 'UA' + gen_random_target() if userAccount == 'random' else userAccount
    userName = 'UN' + gen_random_target() if userName == 'random' else userName
    userNo = 'UNO' + gen_random_target() if userNo == 'random' else userNo
    position = 'PS' + gen_random_target() if position == 'random' else position
    with pytest.allure.step(
            "创建用户 roleId={0}，encryLevelCompany={1}，deptIdList={2}，encryLevelDept={3}".format(roleId, encryLevelCompany,
                                                                                             deptIdList,
                                                                                             encryLevelDept)):
        resp = manageBaseTool.createUser(userAccount, userName, userNo, sex, roleId, encryLevelCompany, position,
                                         deptIdList,
                                         encryLevelDept, token, imgId)
        resp.userAccount = userAccount
        return resp


def enableOrDisableUser(userId, status, token):
    with pytest.allure.step("启用禁用用户 userId={0}，status={1}".format(userId, status)):
        return manageBaseTool.enableOrDisableUser(userId, status, token)


def removeUser(userId, token):
    with pytest.allure.step("删除用户 userId={0}".format(userId)):
        return manageBaseTool.removeUser(userId, token)


test_data, ids = load_csv_file(get_dataProvider('createUser.csv'))


@allure.severity("normal")
@allure.feature(u"管理平台_用户管理")
@allure.story(u"测试story_创建用户")
@pytest.mark.parametrize(
    "account,password,userAccount,userName,userNo,sex,roleName,position,labelList,encryLevelCompany,encryLevelDept,imgId,expectedMessage",
    test_data, ids=ids, )
def test_createUser(account, password, userAccount, userName, userNo, sex, roleName, position, labelList,
                    encryLevelCompany, encryLevelDept, imgId, expectedMessage):
    """
    用例描述：创建用户
    """
    token = manageLogin(account, password)('$.data.token')
    deptIds = getDeptTree(labelList, token)
    roleId = getDictInfo('role', roleName, token) if roleName != 'RNnotExist' else '999999'  # 不存在roleId = '999999'
    resp = createUser(userAccount, userName, userNo, sex, roleId, encryLevelCompany, position, deptIds, encryLevelDept,
                      token, imgId)
    assert check_resp_msg(resp, expectedMessage)
    if resp.message is None:  # 用户创建成功之后查询-禁用用户-删除用户
        userAccount = resp.userAccount
        resp = listUserByPage(token, True, roleId, userAccount, deptIds)
        userId = resp.data.list[0].id
        enableOrDisableUser(userId, False, token)
        removeUser(userId, token)


test_data, ids = load_csv_file(get_dataProvider('enableOrDisableUser.csv'))


@allure.severity("normal")
@allure.feature(u"管理平台_用户管理")
@allure.story(u"测试story_启用禁用用户")
@pytest.mark.parametrize("account,password,userId,status,expectedMessage", test_data, ids=ids, )
def test_enableOrDisableUser(account, password, userId, status, expectedMessage):
    """
    用例描述：启用禁用用户
    """
    token = manageLogin(account, password)('$.data.token')
    resp = enableOrDisableUser(userId, status, token)
    assert check_resp_msg(resp, expectedMessage)
    if status != '':
        resp = enableOrDisableUser(userId, not status, token)
        assert check_resp_msg(resp, expectedMessage)


test_data, ids = load_csv_file(get_dataProvider('removeUser.csv'))


@allure.severity("normal")
@allure.feature(u"管理平台_用户管理")
@allure.story(u"测试story_删除用户")
@pytest.mark.parametrize("account,password,userId,expectedMessage", test_data, ids=ids, )
def test_removeUser(account, password, userId, expectedMessage):
    """
    用例描述：删除用户
    """
    token = manageLogin(account, password)('$.data.token')
    resp = removeUser(userId, token)
    assert check_resp_msg(resp, expectedMessage)
