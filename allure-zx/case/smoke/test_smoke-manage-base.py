#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on June 12, 2019
@author: hzhuangfg
'''
from smokeUtils import *
from com.util import gen_random_target
import sys

reload(sys)
sys.setdefaultencoding('utf-8')  # 修改默认的编码模式


def listPage(userName, customerNo, pageNo, pageSize, token):
    with pytest.allure.step("获取角色列表 userName={0}".format(userName)):
        resp = hoolinkBaseTool.listPage(customerNo, pageNo, pageSize, token)
        roleIds = [role.id for role in resp.data.list]
        assert check_value(resp.checker, True)
        return roleIds


def updateRoleStatus(roleId, status, token):
    with pytest.allure.step("更新角色状态 roleId={0}，status={1}".format(roleId, status)):
        resp = hoolinkBaseTool.updateRoleStatus(roleId, status, token)
        assert check_value(resp.checker, True)


def pageByParam(userName, pageNo, pageSize, token):
    with pytest.allure.step("获取用户列表 userName={0}".format(userName)):
        resp = hoolinkBaseTool.pageByParam(pageNo, pageSize, token)
        assert check_value(resp.checker, True)
        userIds = [user.id for user in resp.data.list]
        return userIds


def checkUserLogin(account, password, customerNo, message):
    with pytest.allure.step("用户登录 account={0}， password = {1}， customerNo = {2}".format(account, password, customerNo)):
        resp = hoolinkBaseTool.login(account, password, customerNo)
        assert check_resp_msg(resp, message) is True
        return resp


def userLogout(account, token):
    with pytest.allure.step("用户登出 account={0}，token = {1}".format(account, token)):
        resp = hoolinkBaseTool.logout(token)
        assert check_value(resp.checker, True)
        return resp


def resetPassword(userId, token):
    with pytest.allure.step("重置用户密码 userId={0}".format(userId)):
        resp = hoolinkBaseTool.resetPassword(userId, token)
        assert check_value(resp.checker, True)


def getCurrentRoleMenu(menuList, token):
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
        childrenRoleMenuVOList = [{'menuId': menuId, 'permissionFlag': 1} for menuId in childrenMenuIdList]
        RoleMenuVOList = parentRoleMenuVOList + childrenRoleMenuVOList
        return RoleMenuVOList


def createRole(roleType, roleMenuVOList, token):
    roleName = 'RN' + gen_random_target()
    roleDesc = 'RD' + gen_random_target()
    with pytest.allure.step("创建角色 roleName={0},roleMenuVOList={1}".format(roleName, roleMenuVOList)):
        resp = manageBaseTool.createRole(roleName, roleType, roleMenuVOList, roleDesc, token)
        assert check_value(resp.checker, True)
        resp.roleName = roleName
        return resp.roleName, resp.data


def updateRole(roleId, roleMenuVOList, roleType, token):
    roleName = 'UPRN' + gen_random_target()
    roleDesc = 'UPRD' + gen_random_target()
    with pytest.allure.step(
            "更新角色 roleId={0}，roleName={1}，roleMenuVOList={2}，roleDesc={3}，roleType={4}".format(roleId, roleName,
                                                                                               roleMenuVOList, roleDesc,
                                                                                               roleType)):
        resp = manageBaseTool.updateRole(roleId, roleName, roleMenuVOList, roleDesc, roleType, token)
        assert check_value(resp.checker, True)
        return resp


def getBaseMenu(code, level, token):
    with pytest.allure.step("获取角色菜单权限 code={0}，level={1}".format(code, level)):
        resp = manageBaseTool.getBaseMenu(code, level, token)
        assert check_value(resp.checker, True)
        return [title for title in resp('$..title')]


def updateMangeRoleStatus(roleId, roleStatus, token):
    with pytest.allure.step("禁用、启用角色 roleId={0},roleStatus={1}".format(roleId, roleStatus)):
        resp = manageBaseTool.updateRoleStatus(roleId, roleStatus, token)
        assert check_value(resp.checker, True)
        return resp.data


def listRoleByPage(status, searchValue, token):
    with pytest.allure.step("获取角色列表 status={0}，searchValue={1}".format(status, searchValue)):
        resp = manageBaseTool.listRoleByPage(1, 10, token, status, searchValue)
        return resp


def getUserInfo(token, message):
    with pytest.allure.step("获取管理员用户信息 token={0}，message={1}".format(token, message)):
        resp = manageBaseTool.getUserInfo(token)
        # assert check_value(resp.checker, True)
        assert check_resp_msg(resp, message) is True
        return resp


def getPhoneCode(phone, token):
    with pytest.allure.step("获取手机验证码 phone={0}".format(phone)):
        resp = manageBaseTool.getPhoneCode(phone, token)
        assert check_value(resp.checker, True)


def verifyPhoneCode(phone, code, token):
    with pytest.allure.step("校验手机验证码 phone={0}，code={1}".format(phone, code)):
        resp = manageBaseTool.verifyPhoneCode(phone, code, token)
        assert check_value(resp.checker, True)


def bindPhone(code, phone, token, message):
    with pytest.allure.step("绑定手机号 phone={0}，code={1}".format(phone, code)):
        resp = manageBaseTool.bindPhone(code, phone, token)
        assert check_resp_msg(resp, message) is True


def resetUserPassword(account, passwd, code, token):
    with pytest.allure.step("更新密码 account={0}，password={1}，code={2}".format(account, passwd, code)):
        resp = manageBaseTool.resetUserPassword(account, passwd, code, token)
        assert check_value(resp.checker, True)


@allure.severity("normal")
@allure.feature(u"测试模块_用户管理")
@allure.story(u"测试story_用户登出")
def test_userLogout(userName='test_huangfg', password='123456'):
    """
    用户tester登录，用户登出，获取用户信息提示无权限访问 - 退出登录token未失效
    """
    token = manageLogin(userName, password)('$.data.token')
    userLogout(userName, token)
    # getUserInfo(token,u'无权限访问')


@allure.severity("normal")
@allure.feature(u"测试模块_用户管理")
@allure.story(u"测试story_用户绑定重复手机号")
def test_bindphone(userName='test_huangfg', password='123456', phone='13567100270', code='hoolink2019'):
    """
    用户tester登录，获取用户信息，获取原手机验证码，校验原手机验证码，获取新手机验证码，校验新手机验证码，绑定手机号提示手机号已被绑定，请更换其他手机号
    """
    token = manageLogin(userName, password)('$.data.token')
    resp = getUserInfo(token, None)
    # getPhoneCode(resp.data.phone, token)
    verifyPhoneCode(resp.data.phone, code, token)
    # getPhoneCode(resp.data.phone, token)
    # verifyPhoneCode(resp.data.phone, code, token)
    bindPhone(code, phone, token, u'手机号已被绑定，请更换其他手机号')


@allure.severity("normal")
@allure.feature(u"测试模块_用户管理")
@allure.story(u"测试story_用户绑定重复手机号")
def test_reBindphone(userName='test_huangfg', password='123456', newPhone='13867483863', code='hoolink2019'):
    """
    用户tester登录，获取用户信息，获取手机验证码，校验手机验证码，绑定手机号提示手机号已被绑定，请更换其他手机号
    """
    token = manageLogin(userName, password)('$.data.token')
    resp = getUserInfo(token, None)
    oldPhone = resp.data.phone
    # getPhoneCode(oldPhone, token)
    verifyPhoneCode(oldPhone, code, token)
    bindPhone(code, newPhone, token, None)
    resp = getUserInfo(token, None)
    # getPhoneCode(newPhone, token)
    verifyPhoneCode(resp.data.phone, code, token)
    bindPhone(code, oldPhone, token, None)


@allure.severity("normal")
@allure.feature(u"测试模块_用户管理")
@allure.story(u"测试story_用户登出")
def test_resetUserPassword(account='test_huangfg', password='123456', code='hoolink2019'):
    """
    用户tester登录，获取用户信息，获取手机验证码，校验手机验证码，重置密码
    """
    token = manageLogin(account, password)('$.data.token')
    resp = getUserInfo(token, None)
    # getPhoneCode(resp.data.phone, token)
    verifyPhoneCode(resp.data.phone, code, token)
    resetUserPassword(account, password, code, token)


@allure.severity("normal")
@allure.feature(u"管理平台_用户管理")
@allure.story(u"测试story_创建角色")
def test_createRoleAndDisable(account='test_huangfg', password='123456', roleType=True,
                              menuList=['EDM系统', '部门资料', '管理中心', '用户管理']):
    """
    用户tester登录，获取角色列表，创建角色，获取角色详情，禁用角色，获取角色列表
    """
    token = manageLogin(account, password)('$.data.token')
    roleMenuVOList = getCurrentRoleMenu(menuList, token)
    roleName, roleId = createRole(roleType, roleMenuVOList, token)
    updateMangeRoleStatus(roleId, False, token)
    resp = listRoleByPage("", roleName, token)
    assert check_value(resp.data.list[0].id, roleId)
    assert check_value(resp.data.list[0].roleName, roleName)


def checkUserRoleMenu(userAccount, password, menuList):
    resp = manageLogin(userAccount, password)
    token = resp('$.data.token')
    edm_menu_list = [name for name in resp('$.data.edmRepertory.name')]  # 获取edm菜单
    check_list_include_list(menuList, edm_menu_list)
    title_list = getBaseMenu(None, None, token)  # 获取角色菜单
    check_list_include_list(menuList, title_list)


@allure.severity("normal")
@allure.feature(u"管理平台_用户管理")
@allure.story(u"测试story_角色用户流程")
def test_manageRoleAndUser(account='test_huangfg', password='123456', roleType=True, labelList=[u'晶日', u'信息文控管理体系中心'],
                           encryLevelCompany=1, encryLevelDept=1):
    """
    用户tester登录，获取角色列表，创建角色，获取组织架构树，创建新用户，新用户登录-校验edm、管理中心、云平台权限菜单，更新角色菜单，新用户登录-校验edm、管理中心、云平台权限菜单，禁用创建角色
    """
    menuList = [u'EDM系统', u'部门资源', u'缓存库', u'管理中心', u'用户管理', u'角色管理']  # 角色菜单权限
    token = manageLogin(account, password)('$.data.token')
    roleMenuVOList = getCurrentRoleMenu(menuList, token)
    roleName, roleId = createRole(roleType, roleMenuVOList, token)
    deptIds = getDeptTree(labelList, token)
    resp = createUser(roleId, True, encryLevelCompany, deptIds, encryLevelDept, token, '')
    userAccount = resp.userAccount
    checkUserRoleMenu(userAccount, password, menuList)
    menuList_ = [u'EDM系统', u'部门资源', u'管理中心', u'用户管理', u'hoolink管理平台', u'客户管理']  # 更改角色菜单权限
    roleMenuVOList_ = getCurrentRoleMenu(menuList_, token)
    updateRole(roleId, roleMenuVOList_, roleType, token)
    checkUserRoleMenu(userAccount, password, menuList_)
    updateMangeRoleStatus(roleId, False, token)


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


def createUser(roleId, sex, encryLevelCompany, deptIdList, encryLevelDept, token, imgId):
    userAccount = 'UA' + gen_random_target()
    userName = 'UN' + gen_random_target()
    userNo = 'UNO' + gen_random_target()
    position = 'PS' + gen_random_target()
    with pytest.allure.step(
            "创建用户 roleId={0}，encryLevelCompany={1}，deptIdList={2}，encryLevelDept={3}".format(roleId, encryLevelCompany,
                                                                                             deptIdList,
                                                                                             encryLevelDept)):
        resp = manageBaseTool.createUser(userAccount, userName, userNo, sex, roleId, encryLevelCompany, position,
                                         deptIdList,
                                         encryLevelDept, token, imgId)
        resp.userAccount = userAccount
        return resp


def listUserByPage(token, status, roleId, groupParam, deptId):
    with pytest.allure.step(
            "获取用户列表 status={0}，roleId={1}，groupParam={2}，deptId={3}".format(status, roleId, groupParam, deptId)):
        return manageBaseTool.listUserByPage(1, 10, token, status, roleId, groupParam, deptId)


def enableOrDisableUser(userId, status, token):
    with pytest.allure.step("启用禁用用户 userId={0}，status={1}".format(userId, status)):
        return manageBaseTool.enableOrDisableUser(userId, status, token)


def removeUser(userId, token):
    with pytest.allure.step("删除用户 userId={0}".format(userId)):
        return manageBaseTool.removeUser(userId, token)


def checkManageLogin(account, password, message):
    with pytest.allure.step("登录后台管理系统 account={0}".format(account)):
        resp = manageBaseTool.login(account, password)
        assert check_value(resp.message, message)


@allure.severity("normal")
@allure.feature(u"管理平台_用户管理")
@allure.story(u"测试story_创建用户")
def test_createUser(account='test_huangfg', password='123456', labelList=['晶日', '信息文控管理体系中心'],
                    roleName=u'RN79729543666', encryLevelCompany=1, encryLevelDept=1):
    """
    用户tester登录，获取组织架构树，创建用户，禁用新建用户对应的角色，校验新建用户登录，启用新建用户对应的角色，校验新建用户登录，禁用新建用户，校验新建用户登录，删除新建用户，校验新建用户登录
    """
    token = manageLogin(account, password)('$.data.token')
    deptIds = getDeptTree(labelList, token)
    roleId = getDictInfo('role', roleName, token)
    resp = createUser(roleId, True, encryLevelCompany, deptIds, encryLevelDept, token, '')
    updateMangeRoleStatus(roleId, False, token)
    userAccount = resp.userAccount
    checkManageLogin(userAccount, password, u'该账号已被禁用，请联系管理员')  # 接口返回message错误，应该是改账户对应的角色被禁用
    updateMangeRoleStatus(roleId, True, token)
    checkManageLogin(resp.userAccount, password, None)
    resp = listUserByPage(token, True, roleId, userAccount, '')
    userId = resp.data.list[0].id
    enableOrDisableUser(userId, False, token)
    checkManageLogin(userAccount, password, u'该账号已被禁用，请联系管理员')
    removeUser(userId, token)
    checkManageLogin(userAccount, password, u'账号或密码错误，请重新输入')
