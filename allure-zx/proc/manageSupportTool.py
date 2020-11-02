#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on July 20, 2019
@author: hzhuangfg
'''
from business.manageSupport import *
from check.checkManageSupport import CheckResult
from com.api import logging
from com.util import gen_md5_sign
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式

class manageSupportTool():
    def __init__(self,logId,env='test',http_client=None):
        self.env = env
        self.logId = gen_md5_sign(logId)
        self.projectId = 'manageSupportTool'
        self.managesupport = manageSupport(self.logId,self.env,http_client)
        self.checker = CheckResult(self.logId,self.env,http_client)
        self.http_client = http_client            #locust client or requests cient
        self.logger = Trace('manageBaseTool')

    @logging("manageSupportTool", "getCustomerById")
    def getCustomerById(self, userId, token):
        """
        获取客户信息
        """
        resp = self.managesupport.getCustomerById(userId,token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "listMenu")
    def listMenu(self,token):
        """
        新增客户获取菜单权限列表
        """
        resp = self.managesupport.listMenu(token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "listMenuById")
    def listMenuById(self, ownerId, token):
        """
        获取对应客户菜单权限
        """
        resp = self.managesupport.listMenuById(ownerId,token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "getAllDeviceTree")
    def getAllDeviceTree(self, token, projectId):
        """
        获取全部设备类型
        """
        resp = self.managesupport.getAllDeviceTree(token, projectId).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "getAloneCameraLiveStream")
    def listProjectByParam(self,pageNo, pageSize, token, name):
        """
        获取项目列表
        """
        resp = self.managesupport.listProjectByParam(pageNo, pageSize, token, name).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "listBySceneId")
    def listBySceneId(self,sceneId, token):
        """
        根据场景获取项目权限菜单
        """
        resp = self.managesupport.listBySceneId(sceneId, token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "createProject")
    def createProject(self, scencId, projectName, customerNo, modelId, menuIdList, deviceType, ownerPhone, ownerName, address,
                      description, token, annexIds):
        """
        创建项目
        """
        resp = self.managesupport.createProject(scencId, projectName, customerNo, modelId, menuIdList, deviceType, ownerPhone,
                                                ownerName, address, description, token, annexIds).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "updateProject")
    def updateProject(self, projectId, no, sceneId, name, customerNo, modelId, menuIdList, deviceType, ownerPhone,
                      ownerName, address, description, token, annexIds):
        """
        更新项目
        """
        resp = self.managesupport.updateProject(projectId, no, sceneId, name, customerNo, modelId, menuIdList,
                                                deviceType, ownerPhone, ownerName, address, description, token,
                                                annexIds).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "updateProjectStatus")
    def updateProjectStatus(self,projectId, status, token):
        """
        更新项目状态
        """
        resp = self.managesupport.updateProjectStatus(projectId, status, token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "updateCustomerStatus")
    def updateCustomerStatus(self,userId, status, token):
        """
        禁用、启用客户
        """
        resp = self.managesupport.updateCustomerStatus(userId, status, token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "resetCustomerPassword")
    def resetCustomerPassword(self,userId, token):
        """
        重置客户密码
        """
        resp = self.managesupport.resetCustomerPassword(userId, token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp


    @logging("manageSupportTool", "createCustomer")
    def createCustomer(self, name, no, userAccount, userName, menuIdList, sex, phone, address, description, token):
        """
        创建客户
        """
        resp = self.managesupport.createCustomer(name, no, userAccount, userName, menuIdList, sex, phone, address,
                                                 description, token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "updateCustomer")
    def updateCustomer(self, customerId, ownerId, name, customerNo, userAccount, userName, sex, phone, address,
                       description, token):
        """
        更新客户
        """
        resp = self.managesupport.updateCustomer(customerId, ownerId, name, customerNo, userAccount, userName, sex,
                                                 phone, address, description, token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "listCustomer")
    def listCustomer(self,pageNo,pageSize,token,name,customerNo,userAccount,userName,phone):
        """
        查询客户列表
        """
        resp = self.managesupport.listCustomer(pageNo,pageSize,token,name,customerNo,userAccount,userName,phone).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "listDevice")
    def listDevice(self, pageNo, pageSize, token, customerName, deviceName, deviceNo, deviceStatus, deviceSubTypeId,
                   deviceTypeId, projectName):
        """
        查询设备列表
        """
        resp = self.managesupport.listDevice(pageNo, pageSize, token, customerName, deviceName, deviceNo, deviceStatus,
                                             deviceSubTypeId, deviceTypeId, projectName).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "listDevice")
    def listDeviceEntryRecord(self,pageNo, pageSize, token, projectName, customerName):
        """
        设备录入记录列表
        """
        resp = self.managesupport.listDeviceEntryRecord(pageNo, pageSize, token, projectName, customerName).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "getSearchDeviceResult")
    def getSearchDeviceResult(self, token, projectName, customerName):
        """
        项目或者公司模糊查询下拉列表数据选择
        """
        resp = self.managesupport.getSearchDeviceResult(token, projectName, customerName).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "getWarrantyList")
    def getWarrantyList(self,pageNo, pageSize, token, companyName, projectName):
        """
        获取设备质保列表
        """
        resp = self.managesupport.getWarrantyList(pageNo, pageSize, token, companyName, projectName).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "getWarrantyList")
    def getWarrantyRecordList(self,pageNo, pageSize, token, companyName, projectName):
        """
        获取设备延保记录
        """
        resp = self.managesupport.getWarrantyRecordList(pageNo, pageSize, token, companyName, projectName).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "updateDeviceWarranty")
    def updateDeviceWarranty(self,projectId,deviceSubTypeId,extensionTerm,maintainTime,token):
        """
        更新设备质保
        """
        resp = self.managesupport.updateDeviceWarranty(projectId,deviceSubTypeId,extensionTerm,maintainTime,token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "getUpgradeList")
    def getUpgradeList(self,type, token):
        """
        获取设备升级列表
        """
        resp = self.managesupport.getUpgradeList(type, token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "getDeviceListByNameNo")
    def getDeviceListByNameNo(self, value, token):
        """
        根据设备序列号/设备名称查询具体的设备
        """
        resp = self.managesupport.getDeviceListByNameNo(value, token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "getUpgradeDeviceById")
    def getUpgradeDeviceById(self, deviceId, token):
        """
        根据设备id查询升级设备信息
        """
        resp = self.managesupport.getUpgradeDeviceById(deviceId, token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "getFirmware")
    def getFirmware(self, deviceSubTypeId, sign, version, token):
        """
        获取升级固件
        """
        resp = self.managesupport.getFirmware(deviceSubTypeId, sign, version, token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "startUpgrade")
    def startUpgrade(self, deviceList, deviceSubTypeId, obsId, type, version, versionId, token):
        """
        设备升级
        """
        resp = self.managesupport.startUpgrade(deviceList, deviceSubTypeId, obsId, type, version, versionId, token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageSupportTool", "__dealwithCommResp__")
    def __dealwithCommResp__(self,resp):
        """
        :param resp:
        :return:
        """
        if resp is not None and resp.has_key('data'):
            if resp.status is True:
                return True
        return False

    @logging("manageSupportTool", "__dealwithLocustResp__")
    def __dealwithLocustResp__(self,resp):
        """
        :param resp:
        :return:
        """
        return True if resp is not None and resp.status is True and self.http_client is not None else False


