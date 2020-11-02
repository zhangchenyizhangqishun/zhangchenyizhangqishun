#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on July 20, 2019
@author: hzhuangfg
'''
from business.hoolinkDevice import *
# from check.checkManageSupport import CheckResult
from com.api import logging
from com.util import gen_md5_sign
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式

class hoolinkDeviceTool():
    def __init__(self, logId, env='test', http_client=None):
        self.env = env
        self.logId = gen_md5_sign(logId)
        self.projectId = 'hoolinkDeviceTool'
        self.hoolinkdevice = hoolinkDevice(self.logId,self.env,http_client)
        self.http_client = http_client            #locust client or requests cient
        self.logger = Trace('hoolinkDeviceTool')


    @logging("hoolinkDeviceTool", "getGroupList")
    def getGroupList(self, projectId, token):
        """
        获取分组列表
        """
        resp = self.hoolinkdevice.getGroupList(projectId, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkDeviceTool", "listTodayPlan")
    def listTodayPlan(self, token):
        """
        获取当天计划
        """
        resp = self.hoolinkdevice.listTodayPlan(token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkDeviceTool", "dimming")
    def dimming(self, projectId, checkPassword, dimming, lightIds, token):
        """
        单灯调光
        """
        checkPassword = get_cloud_pwd_need_md5(checkPassword)
        resp = self.hoolinkdevice.dimming(projectId, checkPassword, dimming, lightIds, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkDeviceTool", "getLightList")
    def getLightList(self, projectId, token, status, deviceName, groupId):
        """
        获取单灯列表
        """
        resp = self.hoolinkdevice.getLightList(projectId, token, status, deviceName, groupId).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkDeviceTool", "detailLightHistory")
    def detailLightHistory(self,bizId, cmdResult, token):
        """
        获取单灯操作历史详情
        """
        resp = self.hoolinkdevice.detailLightHistory(bizId, cmdResult, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkDeviceTool", "lightPageListBizReqHistory")
    def lightPageListBizReqHistory(self, projectId, operationType, beginTime, endTime, pageNo, pageSize, token):
        """
        分页查询单灯操作记录列表
        """
        resp = self.hoolinkdevice.lightPageListBizReqHistory(projectId, operationType, beginTime, endTime, pageNo, pageSize, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkDeviceTool", "strategyPageByParam")
    def strategyPageByParam(self, projectId, pageNo, pageSize, token, status, fuzzyName):
        """
        分页查询策略
        """
        resp = self.hoolinkdevice.strategyPageByParam(projectId, pageNo, pageSize, token, status, fuzzyName).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkDeviceTool", "createStrategy")
    def createStrategy(self, projectId, name, pattern, items, description, token, dayOfWeeks, specialDates):
        """
        创建策略
        """
        resp = self.hoolinkdevice.createStrategy(projectId, name, pattern, items, description, token, dayOfWeeks,
                                                 specialDates).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkDeviceTool", "deleteStrategy")
    def deleteStrategy(self, projectId, strategyId, checkPassword, token):
        """
        删除策略
        """
        checkPassword = get_cloud_pwd_need_md5(checkPassword)
        resp = self.hoolinkdevice.deleteStrategy(projectId, strategyId, checkPassword, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkDeviceTool", "updateStrategyStatus")
    def updateStrategyStatus(self, projectId, strategyId, checkPassword, status, token):
        """
        启用/禁用策略
        """
        checkPassword = get_cloud_pwd_need_md5(checkPassword)
        resp = self.hoolinkdevice.updateStrategyStatus(projectId, strategyId, checkPassword, status, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkDeviceTool", "updateStrategy")
    def updateStrategy(self, strategyId, projectId, name, pattern, items, description, token, dayOfWeeks, specialDates):
        """
        更新策略
        """
        resp = self.hoolinkdevice.updateStrategy(strategyId, projectId, name, pattern, items, description, token,
                                                 dayOfWeeks, specialDates).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp


    @logging("hoolinkDeviceTool", "getStrategy")
    def getStrategy(self, projectId, strategyId, token):
        """
        查询策略
        """
        resp = self.hoolinkdevice.getStrategy(projectId, strategyId, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkDeviceTool", "getStrategyForUpdate")
    def getStrategyForUpdate(self, projectId, strategyId, token):
        """
        更新策略页面
        """
        resp = self.hoolinkdevice.getStrategyForUpdate(projectId, strategyId, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkDeviceTool", "getStrategyConflictDevice")
    def getStrategyConflictDevice(self, projectId, devices, token):
        """
        获取冲突策略详情
        """
        resp = self.hoolinkdevice.getStrategyConflictDevice(projectId, devices, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkDeviceTool", "forcedStrategyToEnable")
    def forcedStrategyToEnable(self, projectId, strategyId, checkPassword, token):
        """
        强制开启策略
        """
        resp = self.hoolinkdevice.forcedStrategyToEnable(projectId, strategyId, checkPassword, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkDeviceTool", "listStrategyLightById")
    def listStrategyLightById(self, itemId, projectId, token):
        """
        设备穿梭框
        """
        resp = self.hoolinkdevice.listStrategyLightById(itemId, projectId, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkDeviceTool", "__dealwithCommResp__")
    def __dealwithCommResp__(self,resp):
        """
        :param resp:
        :return:
        """
        if resp is not None and resp.has_key('data'):
            if resp.status is True:
                return True
        return False

    @logging("hoolinkDeviceTool", "__dealwithLocustResp__")
    def __dealwithLocustResp__(self,resp):
        """
        :param resp:
        :return:
        """
        return True if resp is not None and resp.status is True and self.http_client is not None else False


