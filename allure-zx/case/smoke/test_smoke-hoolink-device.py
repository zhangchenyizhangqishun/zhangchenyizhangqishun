#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on July 28, 2019
@author: hzhuangfg
'''
from smokeUtils import *
from com.util import gen_random_target
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式

def getGroupList(projectId,token):
    with pytest.allure.step("获取分组列表 projectId={0}".format(projectId)):
        return hoolinkDeviceTool.getGroupList(projectId, token)

def getLightList(projectId, token, deviceName='', status=0, groupId=''):
    with pytest.allure.step(
            "获取单灯列表 projectId={0}，status={1}，deviceName={2}，groupId={3}".format(projectId, status, deviceName,
                                                                                groupId)):
        return hoolinkDeviceTool.getLightList(projectId, token, status, deviceName, groupId)

def dimming(projectId, checkPassword, dimming, lightIds, token, message):
    with pytest.allure.step(
            "单灯调光 checkPassword={0}，dimming={1}，lightIds={2}".format(checkPassword, dimming, lightIds)):
        resp = hoolinkDeviceTool.dimming(projectId, checkPassword, dimming, lightIds, token)
        assert check_value(resp.checker, True)
        assert check_value(resp.message, message)

def detailLightHistory(bizId, cmdResult, token):
    with pytest.allure.step("获取单灯操作历史详情 bizId={0}，cmdResult={1}".format(bizId, cmdResult)):
        resp = hoolinkDeviceTool.detailLightHistory(bizId, cmdResult, token)
        assert check_value(resp.checker, True)
        return resp

def lightPageListBizReqHistory(projectId, operationType, beginTime, endTime, token):
    pageNo = 1
    pageSize = 10
    with pytest.allure.step(
            "分页查询单灯操作记录列表 projectId={0}，operationType={1}，beginTime={2}，endTime={3}".format(projectId, operationType,
                                                                                            beginTime, endTime)):
        return hoolinkDeviceTool.lightPageListBizReqHistory(projectId, operationType, beginTime, endTime, pageNo, pageSize, token)

def strategyPageByParam(projectId, pageNo, pageSize, token, fuzzyName='',status="true"):
    with pytest.allure.step("分页查询策略 projectId={0}，status={1}，fuzzyName={2}".format(projectId, status, fuzzyName)):
        return hoolinkDeviceTool.strategyPageByParam(projectId, pageNo, pageSize, token, status, fuzzyName)

def createStrategy(projectId, deviceIds, dimmingValue, pattern, token):
    name = 'strategy_' + gen_random_target()
    description = 'strategyDesc' + gen_random_target()
    nowTime = datetime.now().strftime('%Y-%m-%d %H:%M') + ':00'               # 将当前时间秒数都调成00
    startTime = HumanDateTime(nowTime).add_minute(1).strftime('%H:%M:%S')
    endTime = HumanDateTime(nowTime).add_minute(2).strftime('%H:%M:%S')
    subItems = [{'deviceIds': deviceIds, 'dimmingValue': dimmingValue}]
    items = [{'startTime': startTime, 'endTime': endTime, 'subItems': subItems}]
    specialDates = datetime.now().strftime('%Y-%m-%d')                      # 特殊日期
    dayOfWeeks = [1, 3, 5]                                                  # 自定义特定日期
    specialDates = [] if pattern == '1' or pattern == 2 else specialDates
    dayOfWeeks = [1, 2, 3, 4, 5, 6, 7] if pattern == '1' else dayOfWeeks    # 每天
    dayOfWeeks = [] if pattern == '3' else dayOfWeeks
    with pytest.allure.step(
            "创建策略 projectId={0}，name={1}，pattern={2}，description={3}，dayOfWeeks={4}，specialDates={5}".format(projectId,
                                                                                                             name,
                                                                                                             pattern,
                                                                                                             description,
                                                                                                             dayOfWeeks,
                                                                                                             specialDates)):
        return hoolinkDeviceTool.createStrategy(projectId, name, pattern, items, description, token, dayOfWeeks, specialDates).data

def updateStrategyStatus(projectId, strategyId, checkPassword, status, token):
    with pytest.allure.step("启用/禁用策略 strategyId={0}，status={1}".format(strategyId, status)):
        resp = hoolinkDeviceTool.updateStrategyStatus(projectId, strategyId, checkPassword, status, token)
        assert check_value(resp.checker, True)
        return resp

def deleteStrategy(projectId, strategyId, checkPassword, token, message):
    with pytest.allure.step("删除策略 strategyId={0}，checkPassword={1}".format(strategyId, checkPassword)):
        resp = hoolinkDeviceTool.deleteStrategy(projectId, strategyId, checkPassword, token)
        assert check_value(resp.message, message)


def getStrategyConflictDevice(projectId, devices, token):
    with pytest.allure.step("获取冲突策略设备详情 projectId={0}，devices={1}".format(projectId, devices)):
        resp = hoolinkDeviceTool.getStrategyConflictDevice(projectId, devices, token)
        assert check_value(resp.checker, True)
        return resp

def forcedStrategyToEnable(projectId, strategyId, checkPassword, token):
    with pytest.allure.step("强制开启策略 projectId={0}，strategyId={1}".format(projectId, strategyId)):
        resp = hoolinkDeviceTool.forcedStrategyToEnable(projectId, strategyId, checkPassword, token)
        assert check_value(resp.checker, True)
        return resp

def getStrategyForUpdate(projectId, strategyId, token):
    with pytest.allure.step("更新策略页面 projectId={0}，strategyId={1}".format(projectId, strategyId)):
        resp = hoolinkDeviceTool.getStrategyForUpdate(projectId, strategyId, token)
        assert check_value(resp.checker, True)
        return resp

def getStrategy(projectId, strategyId, token):
    with pytest.allure.step("获取策略详情 projectId={0}，strategyId={1}".format(projectId, strategyId)):
        resp = hoolinkDeviceTool.getStrategy(projectId, strategyId, token)
        assert check_value(resp.checker, True)
        return resp

@allure.severity("normal")
@allure.feature(u"测试模块_单灯模块")
@allure.story(u"测试story_单灯调光")
def test_lightDimming(account='huangfg',password='123456',customerNo='zhangxiao', projectId=514, dimmingValue=25):
    """
    单灯调光流程：用户tester登录，获取单灯列表，单灯调光，校验单灯调光
    """
    token = login(account, password, customerNo)('$.data.token')
    resp = getLightList(projectId, token)
    lightIds = [lightId for lightId in resp('$..id')]
    dimming(projectId, password, dimmingValue, lightIds, token, None)
    lightPageListBizReqHistory(projectId, u'调光', '', '', token)

@allure.severity("normal")
@allure.feature(u"测试模块_策略管理")
@allure.story(u"测试story_重复删除策略")
def test_deleteStrategy(account='huangfg',password='123456',customerNo='zhangxiao',projectId=514,pattern='1'):
    """
    重复删除策略流程：用户tester登录，获取单灯列表，创建策略，删除策略，再次删除策略提示系统错误
    """
    token = login(account, password, customerNo)('$.data.token')
    resp = getLightList(projectId, token)
    deviceIds = [lightId for lightId in resp('$..id')]
    strategyId = createStrategy(projectId, deviceIds, 75, pattern, token)
    deleteStrategy(projectId, strategyId, password, token, None)
    deleteStrategy(projectId, strategyId, password, token, u'系统错误')


@allure.severity("normal")
@allure.feature(u"测试模块_策略管理")
@allure.story(u"测试story_策略操作")
def test_strategyFlow(account='huangfg',password='123456',customerNo='zhangxiao',projectId=514,pattern='1'):
    """
    策略操作流程：用户tester登录，获取单灯列表，创建策略1，启用策略1，创建策略2，启用策略2，判断策略冲突，获取冲突策略设备详情并校验，强制开启策略2，检验策略2启用状态、策略1禁用状态，删除策略1，删除策略2
    """
    token = login(account, password, customerNo)('$.data.token')
    resp = getLightList(projectId, token)
    deviceIds = [lightId for lightId in resp('$..id')]
    strategyId1 = createStrategy(projectId, deviceIds, 75, pattern, token)
    updateStrategyStatus(projectId, strategyId1, password, True, token)
    strategyId2 = createStrategy(projectId, deviceIds, 25, pattern, token)
    resp = updateStrategyStatus(projectId, strategyId2, password, True, token)
    devices = [device for device in resp('$..devices')]                         #"devices": [{"status": true, "id": 31413}, {"status": true, "id": 31414}, {"status": true, "id": 31415}, {"status": true, "id": 31416}]}
    getStrategyConflictDevice(projectId, devices, token)
    forcedStrategyToEnable(projectId, strategyId2, password, token)
    status1 = getStrategy(projectId, strategyId1, token).data.status
    assert check_value(status1, False)
    status2 = getStrategy(projectId, strategyId2, token).data.status
    assert check_value(status2, True)
    deleteStrategy(projectId, strategyId1, password, token, None)
    deleteStrategy(projectId, strategyId2, password, token, None)


# @allure.severity("normal")
# @allure.feature(u"测试模块_项目管理")
# @allure.story(u"测试story_修改项目责任人")
# def test_updateOwnerName(account='huangfg',password='888888',customerNo='1001',ownerName='fuxiuxia'):
#     """
#     用户tester登录，获取项目列表，模糊查询用户名，如果匹配修改项目责任人，更新之后查询项目详情，校验项目责任人和手机号
#     """
#     token = login(account, password, customerNo)('$.data.token')
#     resp = listProject(account, 1, 10, token)
#     for project in resp.data.list:
#         projectId = project.id
#         names = readOwnerName(customerNo, ownerName, token)
#         ownerPhone = gen_random_target('mobile')
#         updateOwnerName(projectId,names[0],ownerPhone,token)
#         resp = getProjectById(projectId, token)
#         check_value(ownerName, resp.data.ownerName)
#         check_value(ownerPhone, resp.data.ownerPhone)


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


# @allure.severity("normal")
# @allure.feature(u"测试模块_角色管理")
# @allure.story(u"测试story_禁用角色")
# def test_disableRoleAndUserLogin(userName='huangfg',password='888888',customerNo='1001',init_password='123456',pageNo=1, pageSize=10):
#     """
#     用户tester登录，获取角色列表，禁用角色，查询角色下用户列表，获取用户信息，用户testerA登录提示角色被禁用，查询用户禁用角色是否包含角色A，启用角色，用户testerA登录登录成功
#     """
#     token = login(userName, password, customerNo)('$.data.token')
#     roleIds = listPage(userName,customerNo,pageNo,pageSize,token)
#     for roleId in roleIds:
#         updateRoleStatus(roleId,False,token)
#     for userId in pageByParam(userName,pageNo,pageSize,token):
#         userLoginInRole(userId,roleIds,token,init_password,u'该账户所属角色已被禁用，请联系管理员')
#     for roleId in roleIds:
#         updateRoleStatus(roleId,True,token)
#     for userId in pageByParam(userName,pageNo,pageSize,token):
#         userLoginInRole(userId, roleIds, token, init_password, None)
#
# @allure.severity("normal")
# @allure.feature(u"测试模块_用户管理")
# @allure.story(u"测试story_禁用用户")
# def test_disableUserAndUserLogin(userName='huangfg',password='888888',customerNo='1001',init_password='123456',pageNo=1, pageSize=10):
#     """
#     用户tester登录，获取用户列表，查询用户详情，重置密码，禁用用户A，用户testerA登录提示账户已被禁用，启用用户A，用户testerA登录登录成功
#     """
#     token = login(userName, password,customerNo)('$.data.token')
#     for userId in pageByParam(userName,pageNo,pageSize,token):
#         resp = getForUpdate(userId,token)
#         resetPassword(userId, token)
#         updateStatus(userId, False, token)
#         userLogin(resp.data.account,init_password,resp.data.customerNo,u'账户已被禁用，请联系管理员')
#         updateStatus(userId, True, token)
#         userLogin(resp.data.account, init_password, resp.data.customerNo, None)
#
#
# @allure.severity("normal")
# @allure.feature(u"测试模块_用户管理")
# @allure.story(u"测试story_创建用户")
# def test_createRoleAndEdit(userName='huangfg',password='888888',customerNo='1001',init_password='123456',readonly=True,sex=True):
#     """
#     用户tester登录，获取角色列表，创建角色，获取角色详情，根据创建角色创建用户，禁用用户，用户testerA登录提示账户已被禁用，启用用户，用户testerA登录登录成功，删除用户，用户testerA登录登录提示登录账号或密码不正确
#     """
#     token = login(userName, password,customerNo)('$.data.token')
#     currencyMenuIds = listByCustomerNo(customerNo,token)
#     roleId = createRole(customerNo, currencyMenuIds, token, readonly)
#     getRoleById(roleId,token)
#     userId,account = createUser(roleId,sex,token)
#     updateStatus(userId, False, token)
#     userLogin(account, init_password,customerNo, u'账户已被禁用，请联系管理员')
#     updateStatus(userId, True, token)
#     resp = userLogin(account, init_password, customerNo, None)
#     assert check_value(resp.data.resetPassword,True)                        #新用户登录重置密码
#     tokenA = resp('$.data.token')
#     resetPasswordForLogin(password, tokenA)
#     resp = userLogin(account, password, customerNo, None)
#     assert check_value(resp.data.resetPassword, False)
#     removeUser(userId, token)
#     userLogin(account, init_password, customerNo, u'登录账号或密码不正确') #当用户被删除时，返回登录账号或密码不正确





