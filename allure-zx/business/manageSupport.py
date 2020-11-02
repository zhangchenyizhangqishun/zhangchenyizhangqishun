#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
Created on June 20, 2019
@author: hzhuangfg
'''
import json
from Config import get_manage_url
from com.util import *
from com.Lib import *
from engine.runner import Runner
from com.api import request,logging

class manageSupport(object):
    def __init__(self, logId, env='test', http_client=None):
        self.appid = self.logId = logId
        self.base_url = get_manage_url(env)
        self.http_client = http_client
        self.runner = Runner(http_client)
        self.common_params = {"http_client_session": self.http_client}
        self.logger = Trace('base')

    @logging("manageSupport", "getCustomerById")
    @request(url='/api/manage-support/web/customer/getById', method='post', headers={"Content-Type": "application/json"})
    def getCustomerById(self, userId, token):
        """
        获取客户信息
        :param userId:
        :param token:
        :return:
        """
        params = {'data': userId, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("manageSupport", "listMenu")
    @request(url='/api/manage-support/web/customer/listMenu', method='post',headers={"Content-Type": "application/json"})
    def listMenu(self, token):
        """
        新增客户获取菜单权限列表
        """
        params = {"X-Token": token}
        return self.__joinParamKey__(params)


    @logging("manageSupport", "listMenuById")
    @request(url='/api/manage-support/web/customer/listMenuById', method='post',headers={"Content-Type": "application/json"})
    def listMenuById(self, ownerId, token):
        """
        获取对应客户菜单权限
        """
        params = {'data':ownerId,"X-Token": token}
        return self.__joinParamKey__(params)


    @logging("manageSupport", "updateProjectStatus")
    @request(url='/api/manage-support/web/project/updateStatus', method='post',headers={"Content-Type": "application/json"})
    def updateProjectStatus(self, projectId, status, token):
        """
        更新项目状态
        :param projectId:
        :param status:False True
        :return:
        """
        params = {"projectId": projectId, "status":status,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageSupport", "getAllDeviceTree")
    @request(url='/api/manage-support/web/project/getAll', method='post',headers={"Content-Type": "application/json"})
    def getAllDeviceTree(self, token, projectId=''):
        """
        获取全部设备类型
        :param projectId:
        :return:
        """
        params = {"X-Token": token}
        params = dict(params, **{'projectId': projectId}) if projectId else params
        return self.__joinParamKey__(params)

    @logging("manageSupport", "listByParam")
    @request(url='/api/manage-support/web/project/listByParam', method='post',headers={"Content-Type": "application/json"})
    def listProjectByParam(self, pageNo, pageSize, token, name=''):
        """
        获取项目列表
        """
        params = {"pageNo": pageNo,"pageSize":pageSize, "X-Token": token}
        params = dict(params, **{'name': name}) if name else params
        return self.__joinParamKey__(params)

    @logging("manageSupport", "listBySceneId")
    @request(url='/api/manage-support/web/project/listBySceneId', method='post',headers={"Content-Type": "application/json"})
    def listBySceneId(self, sceneId, token):
        """
        根据场景获取项目权限菜单
        """
        params = {"sceneId": sceneId, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageSupport", "createProject")
    @request(url='/api/manage-support/web/project/create', method='post',headers={"Content-Type": "application/json"})
    def createProject(self, scencId,projectName,customerNo,modelId,menuIdList,deviceType,ownerPhone,ownerName,address,description,token,annexIds=[]):
        """
        创建项目
        """
        params = {'name':projectName,'scencId':scencId,'customerNo':customerNo,'menuId':menuIdList,'modelId':modelId,'ownerPhone':ownerPhone,
                  'address': address, 'description':description,'ownerName':ownerName,'deviceType':deviceType,"X-Token": token}
        params = dict(params, **{'annexIds': annexIds}) if annexIds else params
        return self.__joinParamKey__(params)

    @logging("manageSupport", "updateProject")
    @request(url='/api/manage-support/web/project/update', method='post',headers={"Content-Type": "application/json"})
    def updateProject(self, projectId,no,sceneId,name,customerNo,modelId,menuIdList,deviceType,ownerPhone,ownerName,address,description,token,annexIds=[]):
        """
        更新项目
        """
        params = {'id':projectId,'no':no,'name':name,'scencId':sceneId,'customerNo':customerNo,'menuId':menuIdList,'modelId':modelId,'ownerPhone':ownerPhone,
                  'address': address, 'description':description,'ownerName':ownerName,'deviceType':deviceType,"X-Token": token}
        params = dict(params, **{'annexIds': annexIds}) if annexIds else params
        return self.__joinParamKey__(params)

    @logging("manageSupport", "updateCustomerStatus")
    @request(url='/api/manage-support/web/customer/updateCustomerStatus', method='post',headers={"Content-Type": "application/json"})
    def updateCustomerStatus(self, userId, status, token):
        """
        禁用、启用客户
        :param id:
        :param status: 1表示启用，0表示禁用
        :param token:
        :return:
        """
        params = {'id': userId, 'status':status, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("manageSupport", "resetCustomerPassword")
    @request(url='/api/manage-support/web/customer/resetPassword', method='post',headers={"Content-Type": "application/json"})
    def resetCustomerPassword(self, userId, token):
        """
        重置客户密码
        :param userId:
        :return:
        """
        params = {'data': userId,'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("manageSupport", "createCustomer")
    @request(url='/api/manage-support/web/customer/create', method='post',headers={"Content-Type": "application/json"})
    def createCustomer(self, name,no,userAccount,userName,menuIdList,sex,phone,address,description,token):
        """
        创建客户
        """
        params = {'name':name,'no':no,'userAccount':userAccount,'menuIdList':menuIdList,'userName':userName,'phone':phone,
                  'address': address, 'description':description,'sex':sex,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageSupport", "updateCustomer")
    @request(url='/api/manage-support/web/customer/update', method='post',headers={"Content-Type": "application/json"})
    def updateCustomer(self,customerId,ownerId,name,customerNo,userAccount,userName,sex,phone,address,description,token):
        """
        更新客户信息
        """
        params = {'id':customerId,'ownerId':ownerId,'name':name,'no':customerNo,'userAccount':userAccount,'sex':sex,'userName':userName,'phone':phone,
                  'address': address, 'description':description,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageSupport", "listCustomer")
    @request(url='/api/manage-support/web/customer/list', method='post',headers={"Content-Type":"application/json"})
    def listCustomer(self,pageNo, pageSize, token, name='',customerNo='',userAccount='',userName='',phone=''):
        """
        查询客户列表
        """
        params = {'pageNo': pageNo, 'pageSize': pageSize, 'name': name, 'no': customerNo, 'userAccount': userAccount,
                'userName': userName, 'phone': phone,"X-Token": token}
        return self.__joinParamKey__(params)


    @logging("manageSupport", "getWarrantyList")
    @request(url='/api/manage-support/web/deviceWarranty/getWarrantyList', method='post',headers={"Content-Type":"application/json"})
    def getWarrantyList(self,pageNo,pageSize,token,companyName='',projectName=''):
        """
        获取设备质保列表
        """
        params = {"pageNo":pageNo, "pageSize":pageSize,"companyName":companyName,"projectName":projectName, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageSupport", "getWarrantyRecordList")
    @request(url='/api/manage-support/web/deviceWarranty/getRecordList', method='post',headers={"Content-Type":"application/json"})
    def getWarrantyRecordList(self,pageNo,pageSize,token,companyName='',projectName=''):
        """
        获取设备延保记录
        """
        params = {"pageNo":pageNo, "pageSize":pageSize,"companyName":companyName,"projectName":projectName, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageSupport", "getWarrantyList")
    @request(url='/api/manage-support/web/deviceWarranty/update', method='post',headers={"Content-Type":"application/json"})
    def updateDeviceWarranty(self,projectId,deviceSubTypeId,extensionTerm,maintainTime,token):
        """
        更新设备质保
        """
        params = {"projectId":projectId, "deviceSubTypeId":deviceSubTypeId,"extensionTerm":extensionTerm,"maintainTimetoken":maintainTime, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageSupport", "listDevice")
    @request(url='/api/manage-support/web/deviceList/list', method='post', headers={"Content-Type": "application/json"})
    def listDevice(self, pageNo, pageSize, token, customerName, deviceName, deviceNo, deviceStatus, deviceSubTypeId,
                   deviceTypeId, projectName):
        """
        查询设备列表
        """
        params = {'pageNo': pageNo, 'pageSize': pageSize,"X-Token": token}
        params = dict(params, **{'customerName': customerName}) if customerName else params
        params = dict(params, **{'deviceName': deviceName}) if deviceName else params
        params = dict(params, **{'deviceNo': deviceNo}) if deviceNo else params
        params = dict(params, **{'deviceStatus': deviceStatus}) if deviceStatus else params
        params = dict(params, **{'deviceSubTypeId': deviceSubTypeId}) if deviceSubTypeId else params
        params = dict(params, **{'deviceTypeId': deviceTypeId}) if deviceTypeId else params
        params = dict(params, **{'projectName': projectName}) if projectName else params
        return self.__joinParamKey__(params)

    @logging("manageSupport", "listDeviceEntryRecord")
    @request(url='/api/manage-support/web/deviceEntryRecord/getList', method='post', headers={"Content-Type": "application/json"})
    def listDeviceEntryRecord(self, pageNo, pageSize, token, projectName, customerName):
        """
        设备录入记录
        """
        params = {'pageNo': pageNo, 'pageSize': pageSize,"X-Token": token}
        params = dict(params, **{'customerName': customerName}) if customerName else params
        params = dict(params, **{'projectName': projectName}) if projectName else params
        return self.__joinParamKey__(params)


    @logging("manageSupport", "getSearchDeviceResult")
    @request(url='/api/manage-support/web/deviceList/getSearchDeviceResult', method='post', headers={"Content-Type": "application/json"})
    def getSearchDeviceResult(self, token, projectName, customerName):
        """
        项目或者公司模糊查询下拉列表数据选择
        """
        params = {"X-Token": token}
        params = dict(params, **{'customerName': customerName}) if customerName else params
        params = dict(params, **{'projectName': projectName}) if projectName else params
        return self.__joinParamKey__(params)

    @logging("manageSupport", "getUpgradeList")
    @request(url='/api/manage-support/web/upgrade/getUpgradeList', method='post',headers={"Content-Type": "application/json"})
    def getUpgradeList(self, type, token):
        """
        获取设备升级列表
        :param type:0 正常高版本升级 1 强制回滚
        """
        params = {'data':type,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageSupport", "getDeviceListByNameNo")
    @request(url='/api/manage-support/web/upgrade/getDeviceListByNameNo', method='post',headers={"Content-Type": "application/json"})
    def getDeviceListByNameNo(self, value, token):
        """
        根据设备序列号/设备名称查询具体的设备
        :param value:设备序列号或者设备名称，传空代表所有
        """
        params = {'data':value,"X-Token": token}
        return self.__joinParamKey__(params)


    @logging("manageSupport", "getUpgradeDeviceById")
    @request(url='/api/manage-support/web/upgrade/getDeviceById', method='post',headers={"Content-Type": "application/json"})
    def getUpgradeDeviceById(self, deviceId, token):
        """
        根据设备id查询升级设备信息
        :param deviceId:
        """
        params = {'data':deviceId,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageSupport", "getFirmware")
    @request(url='/api/manage-support/web/upgrade/getFirmware', method='post',headers={"Content-Type": "application/json"})
    def getFirmware(self, deviceSubTypeId, sign, version, token):
        """
        获取升级固件
        """
        params = {'deviceSubTypeId':deviceSubTypeId,'sign':sign,'version':version,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageSupport", "startUpgrade")
    @request(url='/api/manage-support/web/upgrade/startUpgrade', method='post',headers={"Content-Type": "application/json"})
    def startUpgrade(self, deviceList, deviceSubTypeId, obsId, type, version, versionId, token):
        """
        设备升级
        """
        params = {'deviceList':deviceList,'deviceSubTypeId':deviceSubTypeId,'obsId':obsId, 'type':type,'version':version,'versionId':versionId,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageSupport", "__joinParamKey__")
    def __joinParamKey__(self, params,method = 'post',**kwargs):
        """
        :param params:
        :param method:
        :param kwargs:
        :return:
        """
        params = dict({'params': params}, **kwargs) if method is 'GET' else {'data': params}
        return dict(params, **self.common_params)
