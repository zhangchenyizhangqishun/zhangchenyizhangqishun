#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on June 14, 2019
@author: hzhuangfg
'''
# from proc.omcTool import omcTool
# from proc.mdcTool import mdcTool
# from proc.factoryTool import factoryTool
# from proc.parkTool import parkTool
from proc.hoolinkBaseTool import hoolinkBaseTool
from proc.manageBaseTool import manageBaseTool
from proc.manageSupportTool import manageSupportTool
from proc.abilityTool import abilityTool
from datetime import datetime
from com.human_time import HumanDateTime
from com.util import gen_random_target,generate_time
from com.api import logging
from fs.Trace import Trace
import pytest
import allure
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式
logId = 'smoke'
env = 'test'
logger = Trace('smokeUtils')
hoolinkBaseTool = hoolinkBaseTool(logId,env)
manageBaseTool = manageBaseTool(logId,env)
manageSupportTool = manageSupportTool(logId,env)
abilitytool = abilityTool(logId,env)
# parkTool = parkTool(logId,env)
# omcTool = omcTool(logId,env)
# mdctool = mdcTool(logId,env)
# factoryTool = factoryTool(logId,env)

@allure.step("用户登录：{0}，{1}")     # 测试步骤，可通过format机制自动获取函数参数
@logging("smokeTest","login")
def login(account,password,customerNo):
    # 获取参数
    paras = vars()
    # 报告中的环境参数，可用于必要环境参数的说明，相同的参数以后者为准
    allure.environment(host="192.168.1.18", test_vars=paras)
    return hoolinkBaseTool.login(account,password,customerNo)

@allure.step("用户登录：{0}，{1}")     # 测试步骤，可通过format机制自动获取函数参数
@logging("singleTest","login")
def manageLogin(account,passwd):
    # 获取参数
    paras = vars()
    # 报告中的环境参数，可用于必要环境参数的说明，相同的参数以后者为准
    allure.environment(host="192.168.1.18", test_vars=paras)
    return manageBaseTool.login(account,passwd)

def check_resp_msg(resp,expectedMessage):
    with pytest.allure.step("测试结果校验：{0} == {1}，{2} == {3}".format(resp.message, expectedMessage,resp.status,resp.checker)):
        return True if resp.message == expectedMessage and resp.status == resp.checker else False

def check_value(actualValue,expectedVaule):
    with pytest.allure.step("测试结果校验：{0} == {1}".format(actualValue,expectedVaule)):
        if type(actualValue) == type(expectedVaule):
            return True if actualValue == expectedVaule else False
        else:
            return True if str(actualValue) == str(expectedVaule) else False

def check_value_include(actualValue,expectedVaule):
    with pytest.allure.step("测试结果校验：{0} 包含 {1}".format(actualValue,expectedVaule)):
        return True if actualValue.find(expectedVaule) != -1 else False

def check_list_include_value(list,vaule):
    with pytest.allure.step("测试结果校验：{0} 包含 {1}".format(list,vaule)):
        return True if vaule in list else False

def check_list_include_list(listA,listB):
    with pytest.allure.step("测试结果校验：{0} 包含 {1}".format(listA,listB)):
        return True if set(listB) <= set(listA) else False

# def check_values(actualValueList,expectedVauleList):
#     with pytest.allure.step("测试结果校验：{0} == {1}".format(actualValueList,expectedVauleList)):
#         for actualValue in actualValueList:
#         return True if actualValue == expectedVaule else False

def gen_dead_line(day):
    nowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    deadline = HumanDateTime(nowTime).add_day(day).strftime('%Y-%m-%d %H:%M:%S')
    return deadline

if __name__ == '__main__':
    from com.json_processor import JSONProcessor
    j = {"status":True,"data":{"conflictMap":{"createSceneName_16863117492":[{"deviceTimeStrategyVO":{"deviceType":"5","onTimeStr":"19:52:00","onTime":"1970-01-01 19:52:00","weekTime":"1,2,3,4,5","manageId":7843,"timeType":2,"strategyId":8255,"offTime":"1970-01-01 19:54:00","offTimeStr":"19:54:00"},"dimmingMap":{},"deviceLights":[{"creator":"test_zx1","created":"2018-12-27T07:32:28.000Z","externalId":477,"lightStatus":2,"subTypeId":19,"enabled":True,"lightMacAddress":"123888","updator":"fuxiuxia22","lightName":"测试单灯1","lightId":324,"dimmingValue":0,"lightNo":"2810","updated":"2019-01-21T07:21:47.000Z"}]}],"createSceneName_41487517755":[{"deviceTimeStrategyVO":{"deviceType":"5","onTimeStr":"19:53:00","onTime":"1970-01-01 19:53:00","weekTime":"1,2,3,4,5","manageId":9924,"timeType":2,"strategyId":10191,"offTime":"1970-01-01 19:55:00","offTimeStr":"19:55:00"},"dimmingMap":{},"deviceLights":[{"creator":"test_zx1","created":"2018-12-27T07:32:28.000Z","externalId":477,"lightStatus":2,"subTypeId":19,"enabled":True,"lightMacAddress":"123888","updator":"fuxiuxia22","lightName":"测试单灯1","lightId":324,"dimmingValue":0,"lightNo":"2810","updated":"2019-01-21T07:21:47.000Z"}]}]}},"message":"场景管理读取成功","msgMode":"PROMPT","indexFlag":None,"errorCode":None,"txId":"7c1a0aacfea846bab1838cf7856f567e"}
    resp = JSONProcessor(j)
    # print resp
    manageIdB = 9925
    for item in resp('$..*[@.manageId is %s].manageId' % manageIdB):
        print 'item = %s'%item
        assert item is None
    # resp('$..*[@.manageId is %s].manageId' % manageIdB)