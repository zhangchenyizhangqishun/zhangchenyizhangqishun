#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on June 12, 2019
@author: hzhuangfg
'''
from business.manageBase import *
from check.checkManageBase import CheckResult
from com.api import logging
from com.util import gen_md5_sign
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式

class manageBaseTool():
    def __init__(self,logId,env='test',http_client=None):
        self.env = env
        self.logId = gen_md5_sign(logId)
        self.projectId = 'hoolink'
        self.managebase = manageBase(self.logId,self.env,http_client)
        self.checker = CheckResult(self.logId,self.env,http_client)
        self.http_client = http_client            #locust client or requests cient
        self.logger = Trace('manageBaseTool')

    @logging("manageBaseTool", "login")
    def login(self,account,password):
        """
        管理中心登录
        """
        password = get_pwd_need_md5(password)
        resp = self.managebase.login(account,password).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageBaseTool", "logout")
    def logout(self,token):
        """
        管理中心登出
        """
        resp = self.managebase.logout(token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageBaseTool", "getUserInfo")
    def getUserInfo(self,token):
        """
        获取管理员信息
        """
        resp = self.managebase.getUserInfo(token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageBaseTool", "getPhoneCode")
    def getPhoneCode(self,phone, token):
        """
        获取手机验证码
        """
        resp = self.managebase.getPhoneCode(phone, token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageBaseTool", "verifyPhoneCode")
    def verifyPhoneCode(self,phone, code, token):
        """
        校验手机验证码
        """
        resp = self.managebase.verifyPhoneCode(phone, code, token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageBaseTool", "bindPhone")
    def bindPhone(self,code,phone,token):
        """
        绑定手机号
        """
        resp = self.managebase.bindPhone(code,phone,token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp


    @logging("manageBaseTool", "resetUserPassword")
    def resetUserPassword(self,account, passwd, code, token):
        """
        重置自己密码
        """
        passwd = get_pwd_need_md5(passwd)
        resp = self.managebase.resetUserPassword(account, passwd, code, token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageBaseTool", "getCurrentRoleMenu")
    def getCurrentRoleMenu(self, token):
        """
        获取用户角色菜单按钮
        """
        resp = self.managebase.getCurrentRoleMenu(token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageBaseTool", "createRole")
    def createRole(self,roleName,roleType,roleMenuVOList,roleDesc,token):
        """
        创建角色
        """
        resp = self.managebase.createRole(roleName,roleType,roleMenuVOList,roleDesc,token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageBaseTool", "updateRoleStatus")
    def updateRoleStatus(self,roleId, roleStatus, token):
        """
        禁用、启用角色
        """
        resp = self.managebase.updateRoleStatus(roleId, roleStatus, token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageBaseTool", "updateRole")
    def updateRole(self,roleId, roleName, roleMenuVOList, roleDesc, roleType, token):
        """
        更新角色
        """
        resp = self.managebase.updateRole(roleId, roleName, roleMenuVOList, roleDesc, roleType, token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageBaseTool", "getBaseMenu")
    def getBaseMenu(self, code, level, token):
        """
        获取角色菜单权限
        """
        resp = self.managebase.getBaseMenu(code, level, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageBaseTool", "updateRole")
    def listRoleByPage(self,pageNo, pageSize, token ,status, searchValue):
        """
        查询角色列表
        """
        resp = self.managebase.listRoleByPage(pageNo, pageSize, token ,status, searchValue).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageBaseTool", "getDeptTree")
    def getDeptTree(self, token):
        """
        获取组织架构树
        """
        resp = self.managebase.getDeptTree(token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageBaseTool", "getDeptTree")
    def getDictInfo(self, key, token):
        """
        获取基础字典值数据
        """
        resp = self.managebase.getDictInfo(key,token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageBaseTool", "listCustomer")
    def listUserByPage(self,pageNo, pageSize, token, status, roleId ,groupParam, deptId):
        """
        查询用户列表
        """
        resp = self.managebase.listUserByPage(pageNo, pageSize, token, status, roleId ,groupParam, deptId).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageBaseTool", "createUser")
    def createUser(self,userAccount, userName, userNo, sex, roleId, encryLevelCompany, position, deptIdList,
                   encryLevelDept, token, imgId):
        """
        创建用户
        """
        resp = self.managebase.createUser(userAccount, userName, userNo, sex, roleId, encryLevelCompany, position, deptIdList,
                   encryLevelDept, token, imgId).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageBaseTool", "enableOrDisableUser")
    def enableOrDisableUser(self,userId, status, token):
        """
        启用禁用用户
        """
        resp = self.managebase.enableOrDisableUser(userId, status, token).json
        resp['checker'] = self.checker.check_enableOrDisableUser(resp, userId, status)
        return resp

    @logging("manageBaseTool", "enableOrDisableUser")
    def removeUser(self,userId, token):
        """
        删除用户
        """
        resp = self.managebase.removeUser(userId, token).json
        resp['checker'] = self.checker.check_removeUser(resp,userId,False)
        return resp
		
    @logging("manageBaseTool", "__dealwithCommResp__")
    def __dealwithCommResp__(self,resp):
        """
        :param resp:
        :return:
        """
        if resp is not None and resp.has_key('data'):
            if resp.status is True:
                return True
        return False

    @logging("manageBaseTool", "__dealwithLocustResp__")
    def __dealwithLocustResp__(self,resp):
        """
        :param resp:
        :return:
        """
        if resp is not None:
            if resp.status is True and self.http_client is not None:
                return True
        return False

