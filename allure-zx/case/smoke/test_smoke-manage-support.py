#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on July 02, 2019
@author: hzhuangfg
'''
from smokeUtils import *
from com.util import gen_random_target
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式

def checkUserLogin(account,password,customerNo,message):
    with pytest.allure.step("用户登录 account={0}， password = {1}， customerNo = {2}".format(account, password, customerNo)):
        resp = hoolinkBaseTool.login(account, password, customerNo)
        assert check_resp_msg(resp, message) is True
        return resp

def createCustomer(menuIdList, token):
    with pytest.allure.step("创建客户 menuIdList={0}".format(menuIdList)):
        name = u'corp' + gen_random_target('letter')
        userName = 'hoolink' + gen_random_target('port')
        no = 'jingri' + gen_random_target()
        userAccount = 'yhm' + gen_random_target('port')
        phone = gen_random_target('mobile')
        address = u'滨江区网商路599号'
        description = 'shit'
        sex = 1
        resp = manageSupportTool.createCustomer(name,no,userAccount,userName,menuIdList,sex,phone,address,description,token)
        assert check_value(resp.checker, True)
        return resp

def updateCustomer(customerId,ownerId, customerNo, userAccount, token):
    with pytest.allure.step("更新客户 customerId={0}， ownerId={1}，customerNo={2}，userAccount={3} ".format(customerId,ownerId,customerNo,userAccount)):
        name = u'upcorp' + gen_random_target('letter')
        userName = 'uphoolink' + gen_random_target('port')
        phone = gen_random_target('mobile')
        address = u'up滨江区网商路599号'
        description = 'update_shit'
        sex = 2
        resp = manageSupportTool.updateCustomer(customerId,ownerId,name,customerNo,userAccount,userName,sex,phone,address,description,token)
        assert check_value(resp.checker, True)
        return resp

def listMenu(menuList,token):
    with pytest.allure.step("获取客户菜单权限列表 menuList={0}".format(menuList)):
        resp = manageSupportTool.listMenu(token)
        assert check_value(resp.checker, True)
        menuIdList = []
        for value in menuList:
            menuIds = [key for key in resp('$..*[@.title is "%s"].key' % value)]
            menuIdList += menuIds
        return menuIdList

def listMenuById(ownerId,token):
    with pytest.allure.step("获取对应客户菜单权限 ownerId={0}".format(ownerId)):
        resp = manageSupportTool.listMenuById(ownerId,token)
        assert check_value(resp.checker, True)
        titleList = [title for title in resp('$..*[@.beSelect is True].title')]     # ['管理中心','项目管理']
        return titleList

def getAllDeviceTree(token, labelList,maintainTime, projectId):
    with pytest.allure.step("获取全部设备类型 label={0}，maintainTime={1}".format(labelList,maintainTime)):
        resp = manageSupportTool.getAllDeviceTree(token, projectId)
        assert check_value(resp.checker, True)
        deviceSubTypeIds = []
        deviceTypeList = []
        for label in labelList:
            deviceSubTypeId = [key for key in resp('$..*[@.label is "%s"].value' % label)]  # 将生成器转换成列表，方便两个列表相加
            deviceSubTypeIds += deviceSubTypeId                                             # [1,2] + [3,4] --> [1,2,3,4]
        for deviceSubTypeId in deviceSubTypeIds:
            deviceTypeList.append({'deviceSubTypeId':deviceSubTypeId,'maintainTime':maintainTime})
        return deviceTypeList

def listBySceneId(sceneId,menuList,token):
    with pytest.allure.step("根据场景获取项目权限菜单 sceneId={0}，menuList={1}".format(sceneId,menuList)):
        resp = manageSupportTool.listBySceneId(sceneId,token)
        assert check_value(resp.checker, True)
        menuIdList = []
        for value in menuList:
            menuIds = [key for key in resp('$..*[@.title is "%s"].key' % value)]
            menuIdList += menuIds
        return menuIdList

def uploadCustom(filePath,token):
    with pytest.allure.step("上传模型文件 filePath={0}".format(filePath)):
        resp = abilitytool.uploadCustom(filePath,token)
        assert check_value(resp.checker, True)
        return resp.data.id

def createProject(sceneId,customerNo,modelId,menuIdList,deviceType,annexIds, token):
    with pytest.allure.step("创建项目 sceneId={0}，customerNo={1}，deviceType={2} menuIdList={3}".format(sceneId,customerNo,deviceType,menuIdList)):
        name = u'project' + gen_random_target('letter')
        ownerName = 'fzr' + gen_random_target('port')
        ownerPhone = gen_random_target('mobile')
        address = u'滨江区网商路599号'
        description = 'shit'
        resp = manageSupportTool.createProject(sceneId,name,customerNo,modelId,menuIdList,deviceType,ownerPhone,ownerName,address,description,token,annexIds)
        assert check_value(resp.checker, True)
        resp['name'] = name
        return resp

def updateProject(projectId,no,sceneId,customerNo,modelId,menuIdList,deviceType,annexIds, token):
    with pytest.allure.step("更新项目 projectId={0}，customerNo={1}，deviceType={2}，menuIdList={3}，no={4}".format(projectId,customerNo,deviceType,menuIdList,no)):
        name = u'upproject' + gen_random_target('letter')
        ownerName = 'upfzr' + gen_random_target('port')
        ownerPhone = gen_random_target('mobile')
        address = u'up滨江区网商路599号'
        description = 'upshit'
        resp = manageSupportTool.updateProject(projectId,no,sceneId,name,customerNo,modelId,menuIdList,deviceType,ownerPhone,ownerName,address,description,token,annexIds)
        assert check_value(resp.checker, True)
        return resp

def listProject(name,token):
    with pytest.allure.step("查询项目列表 name={0}".format(name)):
        pageNo = 1
        pageSize = 10
        resp = manageSupportTool.listProjectByParam(pageNo,pageSize,token,name)
        assert check_value(resp.checker, True)
        return resp

def updateProjectStatus(projectId, status, token):
    with pytest.allure.step("启用-禁用项目 projectId={0}，status={1}".format(projectId,status)):
        resp = manageSupportTool.updateProjectStatus(projectId, status, token)
        assert check_value(resp.checker, True)


def updateCustomerStatus(userId, status, token):
    with pytest.allure.step("启用-禁用客户 userId={0}，status={1}".format(userId,status)):
        resp = manageSupportTool.updateCustomerStatus(userId, status, token)
        assert check_value(resp.checker, True)

def listCustomer(customerNo, token):
    with pytest.allure.step("查询客户列表 customerNo={0}".format(customerNo)):
        name=userAccount=userName=phone=''
        pageNo = 1
        pageSize = 10
        resp = manageSupportTool.listCustomer(pageNo,pageSize,token,name,customerNo,userAccount,userName,phone)
        assert check_value(resp.checker, True)
        return resp


@allure.severity("normal")
@allure.feature(u"测试模块_客户管理")
@allure.story(u"测试story_创建客户")
@pytest.mark.parametrize("account,password,menuList", [
    ('test_huangfg', '123456', [u'个人中心',u'基本信息',u'管理中心',u'角色管理']),
    ('test_huangfg', '123456', [u'个人中心',u'基本信息',u'管理中心',u'用户管理']),
    ('test_huangfg', '123456', [u'管理中心',u'角色管理']),
    ('test_huangfg', '123456', [u'管理中心',u'项目管理']),
])
def test_createCustomerAndUpdate(account,password,menuList):
    """
    创建客户流程：管理员登录，获取客户菜单权限列表，创建客户，客户列表中查询创建客户，校验客户菜单权限，更新客户，禁用客户，客户登录，启用客户，客户登录
    """
    token = manageLogin(account,password)('$.data.token')
    menuIdList = listMenu(menuList,token)
    resp = createCustomer(menuIdList, token)
    userId = resp.data.id
    resp_customer = listCustomer(resp.data.customerNo, token)
    ownerId = resp_customer.data.list[0].ownerId
    titleList = listMenuById(ownerId,token)
    check_value(titleList,menuList)
    updateCustomer(resp.data.id,ownerId, resp.data.customerNo, resp.data.userAccount, token)
    updateCustomerStatus(userId, False, token)
    checkUserLogin(resp.data.userAccount, resp.data.password, resp.data.customerNo, u'账户已被禁用，请联系管理员')
    updateCustomerStatus(userId, True, token)
    checkUserLogin(resp.data.userAccount, resp.data.password, resp.data.customerNo, None)



# @allure.severity("normal")
# @allure.feature(u"测试模块_项目管理")
# @allure.story(u"测试story_创建项目")
# @pytest.mark.parametrize("userName,password,customerNo,sceneId,maintainTime,menuList,labelList,annexIds,filePath", [
#     ('test_huangfg', '123456', 'netease', 1, 1, ['设备中心', '设备管理', '设备分组'], ['鸣志智能照明设备','互灵NB智能照明设备'], [411, 412, 413], r'D:\AI\EDM.zip'),
#     ('test_huangfg', '123456', 'alibaba', 3, 2, ['应用中心', '数字音响', '音频文件'], ['itc一键呼叫','世邦一键呼叫'], [411, 412, 413], r'D:\AI\EDM.zip'),
#     ('test_huangfg', '123456', 'netease', 2, 3, ['应用中心', '智能照明', '操作记录'], ['互灵水质监测设备', '互灵土壤监测设备'], [411, 412, 413], r'D:\AI\EDM.zip'),
# ])
# def test_creatProject(userName, password, customerNo, sceneId, maintainTime, menuList, labelList, annexIds, filePath):
#     """
#     管理员登录，根据场景获取项目权限菜单，获取全部设备类型，上传模型文件，上传附件，创建项目，查询项目列表，更新项目，禁用项目
#     """
#     token = manageLogin(userName, password)('$.data.token')
#     menuIdList = listBySceneId(sceneId,menuList,token)
#     deviceType = getAllDeviceTree(token, labelList, maintainTime, '')
#     modelId = uploadCustom(filePath,token)
#     resp = createProject(sceneId, customerNo, modelId, menuIdList, deviceType, annexIds, token)
#     resp = listProject(resp.name,token)
#     projectId = resp.data.list[0].id
#     no = resp.data.list[0].no
#     updateProject(projectId, no, sceneId, customerNo, modelId, menuIdList, deviceType, annexIds, token)
#     updateProjectStatus(projectId, False, token)


def getUpgradeList(type, token):
    with pytest.allure.step("获取设备升级列表 type={0}".format(type)):
        return manageSupportTool.getUpgradeList(type, token)

def getDeviceListByNameNo(value, token):
    with pytest.allure.step("根据设备序列号/设备名称查询具体的设备 value={0}".format(value)):
        resp = manageSupportTool.getDeviceListByNameNo(value, token)
        deviceIds = resp('$..*[@.deviceName is "%s"].id' % value)
        return next(deviceIds)

def getUpgradeDeviceById(deviceId, token):
    with pytest.allure.step("根据设备id查询升级设备信息 deviceId={0}".format(deviceId)):
        return manageSupportTool.getUpgradeDeviceById(deviceId, token)

def getFirmware(deviceSubTypeId, sign, version, token):
    with pytest.allure.step("获取升级固件 deviceSubTypeId={0}，sign={1}，version={2}".format(deviceSubTypeId,sign, version)):
        return manageSupportTool.getFirmware(deviceSubTypeId, sign, version, token)

def startUpgrade(deviceList, deviceSubTypeId, obsId, type, version, versionId, token):
    with pytest.allure.step("根据设备id查询升级设备信息 deviceSubTypeId={0}，deviceList={1}，version={2}，versionId={3}，obsId={4}".format(deviceSubTypeId,deviceList,version,versionId,obsId)):
        return manageSupportTool.startUpgrade(deviceList, deviceSubTypeId, obsId, type, version, versionId, token)
# @allure.severity("normal")
# @allure.feature(u"冒烟模块_设备管理")
# @allure.story(u"测试story_单个设备升级")
# def test_startUpgrade(account='test_huangfg',password='123456',value='真实监控器02'):
#     """
#     用户tester登录，查询具体的设备，查询升级设备信息，获取升级固件，开始升级
#     """
#     token = manageLogin(account, password)('$.data.token')
#     deviceId = getDeviceListByNameNo(value, token)
#     resp = getUpgradeDeviceById(deviceId, token)
#     deviceInfo = resp.data
#     deviceInfo.deviceMac = deviceInfo.mac
#     del deviceInfo.mac
#     deviceList = [deviceInfo]
#     deviceSubTypeId = deviceInfo.deviceSubTypeId
#     resp = getFirmware(deviceSubTypeId, 0, deviceInfo.versionName, token)
#     firmware = resp.data[0]
#     resp = startUpgrade(deviceList, deviceSubTypeId, firmware.obsId, 0, firmware.version, firmware.id, token)
#     check_value(resp.status,True)

def getSearchDeviceResult(token, projectName, customerName):
    with pytest.allure.step("项目或者公司模糊查询下拉列表数据选择 projectName={0}，customerName={1}".format(projectName,customerName)):
        resp = manageSupportTool.getSearchDeviceResult(token, projectName, customerName)
        return resp('$..name')
@allure.severity("normal")
@allure.feature(u"冒烟模块_设备管理")
@allure.story(u"测试story_查询下拉列表数据")
def test_getSearchDeviceResult(account='test_huangfg',password='123456',projectName='project', customerName=''):
    """
    用户tester登录，查询具体的设备，查询升级设备信息，获取升级固件，开始升级
    """
    token = manageLogin(account, password)('$.data.token')
    resp = getSearchDeviceResult(token, projectName, customerName)
    for name in resp:
        check_value_include(name, projectName)