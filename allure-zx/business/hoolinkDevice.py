#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
Created on July 18, 2019
@author: hzhuangfg
'''
import json
from Config import get_base_url
from com.util import *
from com.Lib import *
from engine.runner import Runner
from com.api import request,logging

class hoolinkDevice(object):

    def __init__(self, logId, env='test', http_client=None):
        self.appid = self.logId = logId
        self.base_url = get_base_url(env)
        self.http_client = http_client
        self.runner = Runner(http_client)
        self.common_params = {"http_client_session": self.http_client}
        self.logger = Trace('hoolinkDevice')


    @logging("hoolinkDevice", "getLightList")
    @request(url='/api/hoolink-rpc/web/light/getLightList', method='post',headers={"Content-Type":"application/json"})
    def getLightList(self, projectId, token, status, deviceName, groupId):
        """
        获取单灯列表
        :param deviceName:
        :param groupId:
        :param projectId:
        :param status:设备状态 0:全部,1:工作中,2:在线,3:故障,4:离线,5:维修中
        :param token:
        :return:
        """
        params = {'projectId': projectId, 'X-Token': token}
        params = dict(params, **{'status': status}) if status else params
        params = dict(params, **{'deviceName': deviceName}) if deviceName else params
        params = dict(params, **{'groupId': groupId}) if groupId else params
        return self.__joinParamKey__(params)

    @logging("hoolinkDevice", "getGroupList")
    @request(url='/api/hoolink-rpc/web/light/getGroupList', method='post',headers={"Content-Type":"application/json"})
    def getGroupList(self, projectId, token):
        """
        "data":[{"id":35,"groupName":"张晓项目一组"},{"id":0,"groupName":"未分组"}]
        获取分组列表
        """
        params = {'data': projectId, 'X-Token': token}
        return self.__joinParamKey__(params)


    @logging("hoolinkDevice", "listTodayPlan")
    @request(url='/api/hoolink-rpc/web/today/listTodayPlan', method='post',headers={"Content-Type": "application/json"})
    def listTodayPlan(self, projectId,token):
        """
        获取当天计划
        """
        params = {'data': projectId, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("hoolinkDevice", "dimming")
    @request(url='/api/hoolink-rpc/web/light/dimming', method='post',headers={"Content-Type": "application/json"})
    def dimming(self, projectId, checkPassword, dimming, lightIds, token):
        """
        单灯调光
        :param checkPassword:
        :param dimming:
        :param lightIds:[31413, 31414]
        :param token:
        :return:
        """
        params = {'projectId': projectId, "checkPassword": checkPassword, 'dimming': dimming, 'lightIds': lightIds, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkDevice", "detailLightHistory")
    @request(url='/api/hoolink-rpc/web/light/detailLightHistory', method='post',headers={"Content-Type": "application/json"})
    def detailLightHistory(self, bizId, cmdResult, token):
        """
        获取单灯操作历史详情
        :param bizId:操作记录id
        :param cmdResult:状态，true成功，false失败
        """
        params = {'bizId': bizId, 'cmdResult': cmdResult, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("hoolinkDevice", "lightPageListBizReqHistory")
    @request(url='/api/hoolink-rpc/web/light/pageListBizReqHistory', method='post',headers={"Content-Type": "application/json"})
    def lightPageListBizReqHistory(self, projectId, operationType, beginTime, endTime, pageNo, pageSize, token):
        """
        分页查询单灯操作记录列表
        :param projectId:项目ID，必填
        :param operationType:操作类型
        :return:
        """
        params = {'projectId': projectId, 'beginTime': beginTime, 'endTime': endTime,
                  'pageNo': pageNo, 'pageSize': pageSize, 'X-Token': token}
        params = dict(params, **{'operationType': operationType}) if operationType else params
        return self.__joinParamKey__(params)

    @logging("hoolinkDevice", "strategyPageByParam")
    @request(url='/api/hoolink-rpc/web/light/strategy/pageByParam', method='post',headers={"Content-Type": "application/json"})
    def strategyPageByParam(self, projectId, pageNo, pageSize, token, status, fuzzyName):
        """
        分页查询策略
        :param fuzzyName:名称，模糊查询
        :param status: 启用，禁用
        :param projectId: 项目ID，必填
        :param token:
        :return:
        """
        params = {'projectId': projectId, 'pageNo': pageNo, 'pageSize': pageSize, 'X-Token': token}
        params = dict(params, **{'fuzzyName': fuzzyName}) if fuzzyName else params
        params = dict(params, **{'status': status}) if status else params
        return self.__joinParamKey__(params)

    @logging("hoolinkDevice", "createStrategy")
    @request(url='/api/hoolink-rpc/web/light/strategy/create', method='post',headers={"Content-Type": "application/json"})
    def createStrategy(self, projectId, name, pattern, items, description, token, dayOfWeeks, specialDates):
        """
        创建策略
        :param items:[{endTime: "00:01", startTime: "00:00", subItems: [{deviceIds: [31415, 31413], dimmingValue: 31}]}]
        :param pattern:重复模式 1每天 2自定义 3特殊
        :param specialDates:["2019-07-16", "2019-07-17", "2019-07-18"]
        :param dayOfWeeks:[1, 2, 3, 4, 5, 6, 7]
        :return:
        """

        # specialDates = [] if pattern == '1' or pattern == 2 else specialDates
        # dayOfWeeks = [1, 2, 3, 4, 5, 6, 7] if pattern == '1' else dayOfWeeks # 每天
        # dayOfWeeks = [] if pattern == '3' else dayOfWeeks
        params = {"projectId": projectId, "name": name, "pattern": pattern, "items": items, "description": description,
                  "dayOfWeeks": dayOfWeeks, "specialDates": specialDates, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkDevice", "deleteStrategy")
    @request(url='/api/hoolink-rpc/web/light/strategy/delete', method='post',headers={"Content-Type": "application/json"})
    def deleteStrategy(self, projectId, strategyId, checkPassword, token):
        """
        删除策略
        """
        params = {'projectId':projectId, 'id': strategyId, 'checkPassword': checkPassword, "X-Token": token}
        return self.__joinParamKey__(params)


    @logging("hoolinkDevice", "updateStrategyStatus")
    @request(url='/api/hoolink-rpc/web/light/strategy/updateStatus', method='post',headers={"Content-Type": "application/json"})
    def updateStrategyStatus(self, projectId, strategyId, checkPassword, status, token):
        """
        启用/禁用策略
        """
        params = {'projectId':projectId, 'id': strategyId, 'checkPassword': checkPassword, 'status': status, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("hoolinkDevice", "updateStrategy")
    @request(url='/api/hoolink-rpc/web/light/strategy/update', method='post',headers={"Content-Type": "application/json"})
    def updateStrategy(self, strategyId, projectId, name, pattern, items, description, token, dayOfWeeks, specialDates):
        """
        更新策略
        :param strategyId:
        :param token:
        :return:
        """
        params = {"id":strategyId,"projectId": projectId, "name": name, "pattern": pattern, "items": items, "description": description,
                  "dayOfWeeks": dayOfWeeks, "specialDates": specialDates, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkDevice", "getStrategy")
    @request(url='/api/hoolink-rpc/web/light/strategy/get', method='post',headers={"Content-Type": "application/json"})
    def getStrategy(self, projectId, strategyId, token):
        """
        查询策略
        """
        params = {'data':strategyId, 'projectId': projectId, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("hoolinkDevice", "getStrategyForUpdate")
    @request(url='/api/hoolink-rpc/web/light/strategy/getForUpdate', method='post',headers={"Content-Type": "application/json"})
    def getStrategyForUpdate(self, projectId, strategyId, token):
        """
        更新策略页面
        """
        params = {'data': strategyId, 'projectId': projectId, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("hoolinkDevice", "getStrategyConflictDevice")
    @request(url='/api/hoolink-rpc/web/light/strategy/getConflictDevice', method='post',headers={"Content-Type": "application/json"})
    def getStrategyConflictDevice(self, projectId, devices, token):
        """
        获取冲突策略详情
        :param devices:[id	设备ID	,status	设备状态]
        :return:
        """
        params = {"projectId": projectId, "devices": devices, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkDevice", "forcedStrategyToEnable")
    @request(url='/api/hoolink-rpc/web/light/strategy/forcedToEnable', method='post',headers={"Content-Type": "application/json"})
    def forcedStrategyToEnable(self, projectId, strategyId, checkPassword, token):
        """
        强制开启策略
        """
        params = {"projectId": projectId, "id": strategyId, "checkPassword": checkPassword, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkDevice", "listStrategyLightById")
    @request(url='/api/hoolink-rpc/web/light/strategy/listLightById', method='post',headers={"Content-Type":"application/json"})
    def listStrategyLightById(self, itemId, projectId, token):
        """
        设备穿梭框
        :param itemId:场景项ID
        """
        params = {"itemId": itemId, "projectId": projectId, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkDevice", "__joinParamKey__")
    def __joinParamKey__(self, params,method='post',**kwargs):
        """
        :param params:
        :param method:
        :param kwargs:
        :return:
        """
        params = dict(params, **{'Pid': params['projectId']}) if params.has_key('projectId') else params
        params = dict({'params': params}, **kwargs) if method is 'GET' else {'data': params}
        return dict(params, **self.common_params)