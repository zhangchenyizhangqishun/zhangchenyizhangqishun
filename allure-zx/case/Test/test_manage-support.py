#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on June 25, 2019
@author: hzhuangfg
'''
import allure
from testUtils import *
from com.util import load_csv_file
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式

def check_resp_msg(resp,expectedMessage):
    with pytest.allure.step("测试结果校验：{0} == {1}".format(resp.message, expectedMessage)):
        return True if (resp.message == expectedMessage or resp.message.find(expectedMessage) != -1) else False

def get_dataProvider(caseDataFileName):
    caseDataDir = r'dataProvider\manage-support'
    currentDir=os.path.normpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
    dataProvider_path=os.path.join(currentDir, caseDataDir,caseDataFileName)
    return dataProvider_path


def checkDataListInclude(resp,target,expect):
    for actual in resp('$.data.list.%s' % target):
        assert check_value_include(actual, expect)

def checkDataList(resp,target,expect):
    for actual in resp('$.data.list[@].%s' % target):
        assert check_value(actual, expect)

def checkListCustomer(resp,customerNo,corpName,userAccount, userName, phone):
    if customerNo:
        checkDataListInclude(resp, 'no', customerNo)
    if corpName:
        checkDataListInclude(resp, 'name', corpName)
    if userAccount:
        checkDataListInclude(resp, 'userAccount', userAccount)
    if userName:
        checkDataListInclude(resp, 'userName', userName)
    if phone:
        checkDataListInclude(resp, 'phone', phone)

def listCustomer(customerNo, token, corpName, userAccount, userName, phone):
    with pytest.allure.step("查询客户列表 customerNo={0}，corpName={1}，userAccount={2}，userName={3}，phone={4}".format(customerNo,corpName,userAccount,userName,phone)):
        resp = manageSupportTool.listCustomer(1,10,token,corpName,customerNo,userAccount,userName,phone)
        assert check_value(resp.checker, True)
        return resp
test_data,ids = load_csv_file(get_dataProvider('listCustomer.csv'))
@allure.severity("normal")
@allure.feature(u"管理平台_客户管理")
@allure.story(u"测试story_查询客户列表")
@pytest.mark.parametrize("account,password,customerNo,corpName,userAccount, userName, phone,expectedMessage",test_data,ids=ids,)
def test_listCustomer(account,password,customerNo,corpName,userAccount, userName, phone,expectedMessage):
    """
    用例描述：查询客户列表
    """
    token = manageLogin(account, password)('$.data.token')
    resp = listCustomer(customerNo, token, corpName, userAccount, userName, phone)
    assert check_resp_msg(resp, expectedMessage)
    checkListCustomer(resp, customerNo, corpName, userAccount, userName, phone)


def checkListDevice(resp, customerName, deviceName, deviceNo, deviceStatus, deviceSubTypeName, deviceTypeId, projectName):
    if customerName:
        checkDataListInclude(resp, 'customerName', customerName)
    if deviceName:
        checkDataListInclude(resp, 'deviceName', deviceName)
    if deviceNo:
        checkDataListInclude(resp, 'deviceNo', deviceNo)
    if deviceStatus:
        checkDataList(resp, 'deviceStatus', deviceStatus)
    if deviceTypeId:
        checkDataList(resp, 'deviceTypeId', deviceTypeId)
    if deviceSubTypeName:
        checkDataList(resp, 'subTypeName', deviceSubTypeName)
    if projectName:
        checkDataListInclude(resp, 'projectName', projectName)

def listDevice(token, customerName, deviceName, deviceNo, deviceStatus, deviceSubTypeId,deviceTypeId, projectName):
    with pytest.allure.step(
            "查询设备列表 customerName={0}，deviceName={1}，deviceNo={2}，deviceStatus={3}，deviceSubTypeId={4}，deviceTypeId={5}，projectName={6}".format(
                    customerName, deviceName, deviceNo, deviceStatus, deviceSubTypeId, deviceTypeId, projectName)):
        return manageSupportTool.listDevice(1, 10, token, customerName, deviceName, deviceNo, deviceStatus, deviceSubTypeId,deviceTypeId, projectName)
test_data,ids = load_csv_file(get_dataProvider('listDevice.csv'))
@allure.severity("normal")
@allure.feature(u"管理平台_设备管理")
@allure.story(u"测试story_查询设备列表")
@pytest.mark.parametrize("account,password, customerName, deviceName, deviceNo, deviceStatus, deviceTypeName, deviceSubTypeName, projectName,expectedMessage",test_data,ids=ids,)
def test_listDevice(account,password, customerName, deviceName, deviceNo, deviceStatus, deviceTypeName, deviceSubTypeName, projectName,expectedMessage):
    """
    用例描述：查询设备列表
    """
    token = manageLogin(account, password)('$.data.token')
    deviceTypeDict = {u'数字监控': '1', u'数字音响': '2', u'一键呼叫': '3', u'智能巡检': '4', u'信息发布': '5', u'智能照明': '7', u'实时广播': '8',
                      u'监控器': '9', u'智能灯杆': '13', u'集中器': '14', u'土壤监测': '15', u'水质监测': '16'}
    deviceSubTypeDict = {u'海康摄像头': '1', u'数字音箱': '2', u'世邦数字音箱': '3', u'itc一键呼叫': '4', u'世邦一键呼叫': '5', u'金万马巡检设备': '6',
                         u'诺瓦显示屏': '7', u'鸣志智能照明设备': '10', u'互灵NB智能照明设备': '11', u'itc数字广播设备': '12', u'世邦数字广播设备': '13'}
    deviceStatusDict = {u'工作中': '1', u'待机': '2', u'故障': '3', u'离线': '4', u'维修中': '5'}
    deviceTypeId = deviceTypeDict[deviceTypeName] if deviceTypeDict.has_key(deviceTypeName) else ''
    deviceSubTypeId = deviceSubTypeDict[deviceSubTypeName] if deviceSubTypeDict.has_key(deviceSubTypeName) else ''
    deviceStatusId = deviceStatusDict[deviceStatus] if deviceStatusDict.has_key(deviceStatus) else ''
    resp = listDevice(token, customerName, deviceName, deviceNo, deviceStatusId, deviceSubTypeId, deviceTypeId, projectName)
    assert check_resp_msg(resp, expectedMessage)
    checkListDevice(resp, customerName, deviceName, deviceNo, deviceStatus, deviceSubTypeName, deviceTypeId, projectName)


def checkListDeviceEntryRecord(resp, customerName, projectName):
    if customerName:
        checkDataListInclude(resp, 'customerName', customerName)
    if projectName:
        checkDataListInclude(resp, 'projectName', projectName)

def listDeviceEntryRecord(token, customerName, projectName):
    with pytest.allure.step("查询设备录入记录 customerName={0}，projectName={1}".format(customerName, projectName)):
        return manageSupportTool.listDeviceEntryRecord(1, 10, token, projectName, customerName)
test_data,ids = load_csv_file(get_dataProvider('listDeviceEntryRecord.csv'))
@allure.severity("normal")
@allure.feature(u"管理平台_设备管理")
@allure.story(u"测试story_查询设备录入记录")
@pytest.mark.parametrize("account,password, customerName, projectName,expectedMessage",test_data,ids=ids,)
def test_listDeviceEntryRecord(account,password, customerName, projectName,expectedMessage):
    """
    用例描述：查询设备录入记录
    """
    token = manageLogin(account, password)('$.data.token')
    resp = listDeviceEntryRecord(token, customerName, projectName)
    assert check_resp_msg(resp, expectedMessage)
    checkListDeviceEntryRecord(resp, customerName, projectName)


def checkListWarrantyList(resp, companyName, projectName):
    if companyName:
        checkDataListInclude(resp, 'companyName', companyName)
    if projectName:
        checkDataListInclude(resp, 'projectName', projectName)
def getWarrantyList(token, companyName, projectName):
    with pytest.allure.step("查询设备质保列表 companyName={0}，projectName={1}".format(companyName, projectName)):
        return manageSupportTool.getWarrantyList(1, 10, token, companyName, projectName)
test_data,ids = load_csv_file(get_dataProvider('getWarrantyList.csv'))
@allure.severity("normal")
@allure.feature(u"管理平台_设备管理")
@allure.story(u"测试story_查询设备质保列表")
@pytest.mark.parametrize("account,password, companyName, projectName,expectedMessage",test_data,ids=ids,)
def test_getWarrantyList(account,password, companyName, projectName,expectedMessage):
    """
    用例描述：查询设备质保列表
    """
    token = manageLogin(account, password)('$.data.token')
    resp = getWarrantyList(token, companyName, projectName)
    assert check_resp_msg(resp, expectedMessage)
    checkListWarrantyList(resp, companyName, projectName)


def getWarrantyRecordList(token, companyName, projectName):
    with pytest.allure.step("查询设备延保记录列表 companyName={0}，projectName={1}".format(companyName, projectName)):
        return manageSupportTool.getWarrantyRecordList(1, 10, token, companyName, projectName)
test_data,ids = load_csv_file(get_dataProvider('getWarrantyRecordList.csv'))
@allure.severity("normal")
@allure.feature(u"管理平台_设备管理")
@allure.story(u"测试story_查询设备延保记录列表")
@pytest.mark.parametrize("account,password, companyName, projectName,expectedMessage",test_data,ids=ids,)
def test_getWarrantyRecordList(account,password, companyName, projectName,expectedMessage):
    """
    用例描述：查询设备延保记录列表
    """
    token = manageLogin(account, password)('$.data.token')
    resp = getWarrantyRecordList(token, companyName, projectName)
    assert check_resp_msg(resp, expectedMessage)
    checkListWarrantyList(resp, companyName, projectName)


def listBySceneId(sceneId,menuList,token):
    with pytest.allure.step("根据场景获取项目权限菜单 sceneId={0}，menuList={1}".format(sceneId,menuList)):
        resp = manageSupportTool.listBySceneId(sceneId,token)
        assert check_value(resp.checker, True)
        menuIdList = []
        for value in menuList:
            menuIds = [key for key in resp('$..*[@.title is "%s"].key' % value)]
            menuIdList += menuIds
        return menuIdList

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

def createProject(sceneId,projectName,customerNo,modelId,menuIdList,deviceType,ownerPhone,ownerName,address,description,token,annexIds):
    with pytest.allure.step("创建项目 sceneId={0}，customerNo={1}，deviceType={2} menuIdList={3}".format(sceneId,customerNo,deviceType,menuIdList)):
        projectName = u'project' + gen_random_target('letter') if projectName == 'random' else projectName
        ownerName = 'fzr' + gen_random_target('port') if ownerName.lower() == 'random' else ownerName
        ownerPhone = gen_random_target('mobile') if ownerPhone.lower() == 'random' else ownerPhone
        address = u'滨江区网商路599号' if address.lower() == 'random' else address
        description = 'descRandom' if description.lower() == 'random' else description
        resp = manageSupportTool.createProject(sceneId,projectName,customerNo,modelId,menuIdList,deviceType,ownerPhone,ownerName,address,description,token,annexIds)
        resp.name = projectName
        return resp
test_data,ids = load_csv_file(get_dataProvider('createProject.csv'))
@allure.severity("normal")
@allure.feature(u"管理平台_用户管理")
@allure.story(u"测试story_创建用户")
@pytest.mark.parametrize("account,password,customerNo,sceneId,projectName,modelId,menuList,labelList,ownerPhone,ownerName,address,description,annexIds,expectedMessage",test_data,ids=ids,)
def test_createProject(account,password,customerNo,sceneId,projectName,modelId,menuList,labelList,ownerPhone,ownerName,address,description,annexIds,expectedMessage):
    """
    用例描述：创建项目
    """
    # labelList = eval(labelList)
    # annexIds = eval(annexIds)
    # menuList = eval(menuList)
    token = manageLogin(account, password)('$.data.token')
    menuIdList = listBySceneId(sceneId, menuList, token)
    deviceType = getAllDeviceTree(token, labelList, 1, '')
    resp = createProject(sceneId,projectName,customerNo,modelId,menuIdList,deviceType,ownerPhone,ownerName,address,description,token,annexIds)
    assert check_resp_msg(resp,expectedMessage)