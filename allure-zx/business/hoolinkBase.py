#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
Created on July 16, 2019
@author: hzhuangfg
'''
import json
from Config import get_base_url
from com.util import *
from com.Lib import *
from engine.runner import Runner
from com.api import request,logging

class hoolinkBase(object):

    def __init__(self, logId, env='test', http_client=None):
        self.appid = self.logId = logId
        self.base_url = get_base_url(env)
        self.http_client = http_client
        self.runner = Runner(http_client)
        self.common_params = {"http_client_session": self.http_client}
        self.logger = Trace('hoolinkBase')

    @logging("hoolinkBase","login")
    @request(url='/api/hoolink-rpc/web/login', method='post',headers={"Content-Type":"application/json"})
    def login(self,account,password,customerNo):
        """
        登录
        """
        params = {"account": account, "password": password,'customerNo':customerNo}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "logout")
    @request(url='/api/hoolink-rpc/web/logout', method='post',headers={"Content-Type":"application/json"})
    def logout(self,token):
        """
        退出登录
        """
        params = {'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "getUserInfo")
    @request(url='/api/hoolink-rpc/web/base/get', method='post',headers={"Content-Type":"application/json"})
    def getUserInfo(self,token):
        """
        获取用户信息
        """
        params = {'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "createUser")
    @request(url='/api/hoolink-rpc/web/user/createUser', method='post',headers={"Content-Type": "application/json"})
    def createUser(self, account, roleId, name, sex,token):
        """
        创建用户
        """
        # areaIds = eval(str(areaIds))
        # projectIds = eval(str(projectIds))      #'[6,9]' --> [6,9]
        params = {"account": account, "name": name, "sex": sex,
                    "roleId": roleId,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "updateBaseName")
    @request(url='/api/hoolink-rpc/web/base/updateName', method='post',headers={"Content-Type": "application/json"})
    def updateBaseName(self, userName, token):
        """
        更新自己姓名
        """
        params = {"data": userName, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "updateUserName")
    @request(url='/api/hoolink-rpc/web/user/updateName', method='post',headers={"Content-Type": "application/json"})
    def updateUserName(self, userId, name, token):
        """
        更新其他用户姓名
        """
        params = {'id': userId, 'name':name, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "updateBaseSex")
    @request(url='/api/hoolink-rpc/web/base/updateSex', method='post',headers={"Content-Type": "application/json"})
    def updateBaseSex(self, userSex, token):
        """
        更新自己性别
        :param userSex: 男True女False
        :param token:
        :return:
        """
        params = {"data": userSex, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "updateUserSex")
    @request(url='/api/hoolink-rpc/web/user/updateSex', method='post',headers={"Content-Type": "application/json"})
    def updateUserSex(self, userId, sex, token):
        """
        更新其他用户性别
        :param id:
        :param sex: 男True女False
        :param token:
        :return:
        """
        params = {'id': userId, 'sex':sex, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "updateRoleStatus")
    @request(url='/api/hoolink-rpc/web/role/updateStatus', method='post',headers={"Content-Type": "application/json"})
    def updateRoleStatus(self, roleId, status, token):
        """
        更新角色状态
        :param roleId:
        :param status:
        :return:
        """
        params = {"roleId": roleId, "status":status,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "listPage")
    @request(url='/api/hoolink-rpc/web/role/listPage', method='post',headers={"Content-Type": "application/json"})
    def listPage(self, customerNo, pageNo, pageSize, token):
        """
        获取角色列表
        """
        params = {'customerNo':customerNo,'pageNo':pageNo,'pageSize':pageSize,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "pageByParam")
    @request(url='/api/hoolink-rpc/web/user/pageByParam', method='post',headers={"Content-Type": "application/json"})
    def pageByParam(self, pageNo, pageSize, token, fuzzyName, fuzzyPhone,fuzzyRole,projectId,status):
        """
        获取用户列表
        """
        params = {'fuzzyName': fuzzyName, 'pageNo': pageNo, 'pageSize': pageSize, 'fuzzyPhone': fuzzyPhone,
                  'fuzzyRole': fuzzyRole, 'projectId': projectId, 'status': status, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "getForUpdate")
    @request(url='/api/hoolink-rpc/web/user/getForUpdate', method='post',headers={"Content-Type": "application/json"})
    def getForUpdate(self, userId, token):
        """
        获取其他用户信息
        :param userId:
        :param token:
        :return:
        """
        params = {"data": userId, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "updateUserRole")
    @request(url='/api/hoolink-rpc/web/user/updateRole', method='post',headers={"Content-Type": "application/json"})
    def updateUserRole(self, userId, roleId, token):
        """
        更新其他用户角色
        """
        params = {'id':userId,'roleId':roleId,'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "listByCustomerNo")
    @request(url='/api/hoolink-rpc/web/menu/listByCustomerNo', method='post',headers={"Content-Type": "application/json"})
    def listByCustomerNo(self, customerNo, token):
        """
        获取角色权限列表
        :param customerNo:客户号
        :return:
        """
        params = {"data": customerNo, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "createRole")
    @request(url='/api/hoolink-rpc/web/role/create', method='post',headers={"Content-Type": "application/json"})
    def createRole(self, customerNo,name,description,currencyMenuIds,token,readonly=True,projectMenuIds=[]):
        """
        创建角色
        :param customerNo:客户号
        :return:
        """
        projectMenus = [{'menuId':menuId,'readonly':readonly,'projectId':0} for menuId in currencyMenuIds]
        params = {"customerNo": customerNo, "name":name,"description":description,"projectMenus":projectMenus,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "updateRole")
    @request(url='/api/hoolink-rpc/web/role/update', method='post',headers={"Content-Type":"application/json"})
    def updateRole(self,roleId,customerNo,name,description,currencyMenuIds,token,readonly=True,projectMenuIds=[]):
        """
        更新角色
        """
        projectMenus = [{'menuId': menuId, 'readonly': readonly, 'projectId': 0} for menuId in currencyMenuIds]
        params = {"id":roleId,"customerNo": customerNo, "name": name, "description": description, "projectMenus": projectMenus,
                  "X-Token": token}
        return self.__joinParamKey__(params)


    @logging("hoolinkBase", "getRoleById")
    @request(url='/api/hoolink-rpc/web/role/getById', method='post',headers={"Content-Type": "application/json"})
    def getRoleById(self, roleId, token):
        """
        获取角色详情
        :param roleId:
        :return:
        """
        params = {"data": roleId, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "removeUser")
    @request(url='/api/hoolink-rpc/web/user/removeUser', method='post',headers={"Content-Type": "application/json"})
    def removeUser(self, userId, token):
        """
        删除用户
        """
        params = {"data": userId, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "updateStatus")
    @request(url='/api/hoolink-rpc/web/user/updateStatus', method='post',headers={"Content-Type": "application/json"})
    def updateStatus(self, userId, status, token):
        """
        禁用、启用用户
        :param id:
        :param sex: 男True女False
        :param token:
        :return:
        """
        params = {'id': userId, 'status':status, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "resetPasswordForLogin")
    @request(url='/api/hoolink-rpc/web/resetPasswordForLogin', method='post',headers={"Content-Type": "application/json"})
    def resetPasswordForLogin(self, newPassword, token):
        """
        新用户登录重置密码
        :param newPassword:
        :param token:
        :return:
        """
        params = {'data': newPassword, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "resetPassword")
    @request(url='/api/hoolink-rpc/web/user/resetPassword', method='post',headers={"Content-Type": "application/json"})
    def resetPassword(self, userId, token):
        """
        重置用户密码
        :param userId:
        :param token:
        :return:
        """
        params = {'data': userId, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "listProject")
    @request(url='/api/hoolink-rpc/web/project/listByRoleId', method='post',headers={"Content-Type": "application/json"})
    def listProject(self, pageNo, pageSize, token):
        """
        查询项目列表
        """
        params = {"pageNo": pageNo, "pageSize":pageSize, "X-Token": token}
        return self.__joinParamKey__(params)


    @logging("hoolinkBase", "readOwnerName")
    @request(url='/api/hoolink-rpc/web/project/readOwnerName', method='post',headers={"Content-Type":"application/json"})
    def readOwnerName(self, customerNo, ownerName, token):
        """
        模糊查询用户名
        """
        params = {"customerNo": customerNo, "ownerName": ownerName,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "updateOwnerName")
    @request(url='/api/hoolink-rpc/web/project/updateOwnerName', method='post',headers={"Content-Type":"application/json"})
    def updateOwnerName(self,projectId,ownerName,ownerPhone,token):
        """
        修改项目责任人
        """
        params = {'id': projectId, 'ownerName': ownerName, 'ownerPhone': ownerPhone,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "readRoleDetail")
    @request(url='/api/hoolink-rpc/web/project/getById', method='post',headers={"Content-Type":"application/json"})
    def getProjectById(self,projectId,token):
        """
        项目详情查询
        """
        params = {"data": projectId, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "sendCaptchaForUpdatePhone")
    @request(url='/api/hoolink-rpc/web/base/sendCaptchaForUpdatePhone', method='post',
             headers={"Content-Type": "application/json"})
    def sendCaptchaForUpdatePhone(self, token):
        """
        修改手机号发送短信
        """
        params = {"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "sendCaptchaForNewPhone")
    @request(url='/api/hoolink-rpc/web/base/sendCaptchaForNewPhone', method='post',
             headers={"Content-Type": "application/json"})
    def sendCaptchaForNewPhone(self, phone, oldCaptcha, token):
        """
        向重新绑定手机号发送短信
        """
        params = {'phone': phone, 'oldCaptcha': oldCaptcha, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "checkCaptchaForUpdatePassword")
    @request(url='/api/hoolink-rpc/web/base/checkCaptchaForUpdatePassword', method='post',
             headers={"Content-Type": "application/json"})
    def checkCaptchaForUpdatePassword(self, vcode, token):
        """
        修改密码验证短信
        """
        params = {"data": vcode, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "checkCaptchaForUpdatePhone")
    @request(url='/api/hoolink-rpc/web/base/checkCaptchaForUpdatePhone', method='post',
             headers={"Content-Type": "application/json"})
    def checkCaptchaForUpdatePhone(self, vcode, token):
        """
        修改手机号验证短信
        """
        params = {"data": vcode, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "updatePhone")
    @request(url='/api/hoolink-rpc/web/base/updatePhone', method='post', headers={"Content-Type": "application/json"})
    def updatePhone(self, captcha, oldCaptcha, phone, token):
        """
        更改绑定手机号
        """
        params = {"captcha": captcha, "oldCaptcha": oldCaptcha, "phone": phone, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "updatePassword")
    @request(url='/api/hoolink-rpc/web/base/updatePassword', method='post',
             headers={"Content-Type": "application/json"})
    def updatePassword(self, captcha, password, token):
        """
        修改密码
        """
        params = {"captcha": captcha, "password": password, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("hoolinkBase", "__joinParamKey__")
    def __joinParamKey__(self, params,method = 'post',**kwargs):
        """
        :param params:
        :param method:
        :param kwargs:
        :return:
        """
        params = dict({'params': params}, **kwargs) if method is 'GET' else {'data': params}
        return dict(params, **self.common_params)