#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on June 12, 2019
@author: hzhuangfg
'''
from business.hoolinkBase import *
from business.gatepay import *
from business.parkRpc import *
from check.checkHoolinkBase import CheckResult
from com.api import logging
from com.json_processor import JSONProcessor
from com.util import gen_random_target
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式

class hoolinkBaseTool():
    def __init__(self,logId,env='test',http_client=None):
        self.env = env
        self.logId = gen_md5_sign(logId)
        self.projectId = 'hoolink'
        self.hoolinkBase = hoolinkBase(self.logId,self.env,http_client)
        self.checker = CheckResult(self.logId,self.env,http_client)
        self.http_client = http_client            #locust client or requests cient
        self.logger = Trace('tool')

    @logging("hoolinkBaseTool","login")
    def login(self,account,password,customerNo):
        """
        登录
        """
        password = get_cloud_pwd_need_md5(password)
        resp = self.hoolinkBase.login(account,password,customerNo).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "logout")
    def logout(self,token):
        """
        退出登录
        """
        resp = self.hoolinkBase.logout(token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "sendCaptchaForUpdatePhone")
    def getUserInfo(self,token):
        """
        获取用户信息
        """
        resp = self.hoolinkBase.getUserInfo(token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "sendCaptchaForUpdatePhone")
    def sendCaptchaForUpdatePhone(self,token):
        """
        修改手机号发送短信
        """
        resp = self.hoolinkBase.sendCaptchaForUpdatePhone(token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "checkCaptchaForUpdatePhone")
    def checkCaptchaForUpdatePhone(self,vcode,token):
        """
        修改手机号验证短信
        """
        resp = self.hoolinkBase.checkCaptchaForUpdatePhone(vcode,token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp


    @logging("hoolinkBaseTool", "sendCaptchaForUpdatePhone")
    def sendCaptchaForNewPhone(self,phone,oldCaptcha,token):
        """
        向重新绑定手机号发送短信
        """
        resp = self.hoolinkBase.sendCaptchaForNewPhone(phone,oldCaptcha,token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "updatePhone")
    def updatePhone(self,captcha,oldCaptcha,phone,token):
        """
        更改绑定手机号
        """
        resp = self.hoolinkBase.updatePhone(captcha,oldCaptcha,phone,token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "updateBaseName")
    def updateBaseName(self,userName, token):
        """
        更新自己姓名
        """
        resp = self.hoolinkBase.updateBaseName(userName, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "updateBaseSex")
    def updateBaseSex(self,userSex, token):
        """
        更新自己性别
        """
        resp = self.hoolinkBase.updateBaseSex(userSex, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp


    @logging("hoolinkBaseTool", "updateBaseSex")
    def updateUserSex(self,userId, sex, token):
        """
        更新其他用户性别
        """
        resp = self.hoolinkBase.updateUserSex(userId, sex, token).json
        resp['checker'] = self.checker.check_updateUserSex(resp,userId,sex)
        return resp


    @logging("hoolinkBaseTool", "updateUserName")
    def updateUserName(self,userId, name, token):
        """
        更新其他用户姓名
        """
        resp = self.hoolinkBase.updateUserName(userId, name, token).json
        resp['checker'] = self.checker.check_updateUserSex(resp,userId,name)
        return resp

    @logging("hoolinkBaseTool", "updateRoleStatus")
    def updateRoleStatus(self,roleId, status, token):
        """
        更新角色状态
        """
        resp = self.hoolinkBase.updateRoleStatus(roleId, status, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "listPage")
    def listPage(self,customerNo, pageNo, pageSize, token):
        """
        获取角色列表
        """
        resp = self.hoolinkBase.listPage(customerNo, pageNo, pageSize, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "pageByParam")
    def pageByParam(self,pageNo, pageSize, token, fuzzyName, fuzzyPhone,fuzzyRole,projectId,status):
        """
        获取用户列表
        """
        resp = self.hoolinkBase.pageByParam(pageNo, pageSize, token ,fuzzyName, fuzzyPhone,fuzzyRole,projectId,status).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "getForUpdate")
    def getForUpdate(self,userId, token):
        """
        获取其他用户信息
        """
        resp = self.hoolinkBase.getForUpdate(userId, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "updateRole")
    def updateUserRole(self,userId, roleId, token):
        """
        更新其他用户角色
        """
        resp = self.hoolinkBase.updateUserRole(userId, roleId, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "listByCustomerNo")
    def listByCustomerNo(self,customerNo, token):
        """
        获取角色列表
        """
        resp = self.hoolinkBase.listByCustomerNo(customerNo, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "createRole")
    def createRole(self,customerNo,currencyMenuIds,token,readonly,name,description):
        """
        创建角色
        """
        # self.logger.debug('currencyMenuIds = %s'%currencyMenuIds)
        resp = self.hoolinkBase.createRole(customerNo,name,description,currencyMenuIds,token,readonly).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "updateRole")
    def updateRole(self,roleId,customerNo,name,description,currencyMenuIds,token,readonly):
        """
        创建角色
        """
        resp = self.hoolinkBase.updateRole(roleId,customerNo,name,description,currencyMenuIds,token,readonly).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "getRoleById")
    def getRoleById(self,roleId, token):
        """
        获取角色详情
        """
        resp = self.hoolinkBase.getRoleById(roleId, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "updateUserPassWord")
    def updatePassword(self,captcha,password,token):
        """
        改密码
        """
        # password = get_pwd_need_md5(password)
        resp = self.hoolinkBase.updatePassword(captcha,password,token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "createUser")
    def createUser(self, account,roleId, name, sex,token):
        """
        创建用户
        """
        resp = self.hoolinkBase.createUser(account, roleId, name, sex,token).json
        resp['checker'] = self.checker.check_createUser(resp,account, roleId, name, sex)
        return resp

    @logging("hoolinkBaseTool", "removeUser")
    def removeUser(self, userId, token):
        """
        删除用户
        """
        resp = self.hoolinkBase.removeUser(userId, token).json
        resp['checker'] = self.checker.check_removeUser(resp,userId, False)
        return resp

    @logging("hoolinkBaseTool", "updateStatus")
    def updateStatus(self, userId, status, token):
        """
        启用、禁用用户
        """
        resp = self.hoolinkBase.updateStatus(userId, status, token).json
        resp['checker'] = self.checker.check_updateStatus(resp,userId, status)
        return resp

    @logging("hoolinkBaseTool", "resetPasswordForLogin")
    def resetPasswordForLogin(self, newPassword, token):
        """
        新用户登录重置密码
        """
        resp = self.hoolinkBase.resetPasswordForLogin(newPassword, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "resetPassword")
    def resetPassword(self, userId, token):
        """
        重置密码
        """
        resp = self.hoolinkBase.resetPassword(userId, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "readCreatedByMeUsers")
    def listProject(self,pageNo, pageSize, token):
        """
        查询项目列表
        """
        resp = self.hoolinkBase.listProject(pageNo, pageSize, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "readSubordinateCreatedUsers")
    def readOwnerName(self,customerNo, ownerName, token):
        """
        模糊查询用户名
        """
        resp = self.hoolinkBase.readOwnerName(customerNo, ownerName, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "deleteUser")
    def updateOwnerName(self,projectId,ownerName,ownerPhone,token):
        """
        修改项目责任人
        """
        resp = self.hoolinkBase.updateOwnerName(projectId,ownerName,ownerPhone,token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "readDisableUsers")
    def getProjectById(self,projectId,token):
        """
        项目详情查询
        """
        resp = self.hoolinkBase.getProjectById(projectId,token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp


    @logging("hoolinkBaseTool", "enableUser")
    def enableUser(self,userId, token):
        """
        启用用户
        """
        resp = self.hoolinkBase.enableUser(userId, token).json
        resp['checker'] = self.checker.check_enableUser(resp,userId)
        return resp

    @logging("hoolinkBaseTool", "createInitData")
    def createInitData(self,token):
        """
        角色数据初始化
        """
        resp = self.hoolinkBase.createInitData(token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("hoolinkBaseTool", "createRoleDetail")
    def createRoleDetail(self,commonMenuList,sceneMenuList,token):
        """
        创建角色
        """
        enabled = True
        roleDesc = u'Desc'+gen_random_target('port')
        roleName = u'Name'+gen_random_target('port')
        resp = self.hoolinkBase.createRoleDetail(enabled,roleDesc,roleName,commonMenuList,sceneMenuList,token).json
        resp['checker'] = self.checker.check_createRoleDetail(resp)
        return resp


    @logging("hoolinkBaseTool", "__dealwithCommResp__")
    def __dealwithCommResp__(self,resp):
        """
        :param resp:
        :return:
        """
        if resp is not None and resp.has_key('data'):
            if resp.status is True:
                return True
        return False

