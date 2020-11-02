#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
Created on June 18, 2019
@author: hzhuangfg
'''
import json
from Config import get_manage_url
from com.util import *
from com.Lib import *
from engine.runner import Runner
from com.api import request,logging

class manageBase(object):

    def __init__(self, logId, env='test', http_client=None):
        self.appid = self.logId = logId
        self.base_url = get_manage_url(env)
        self.http_client = http_client
        self.runner = Runner(http_client)
        self.common_params = {"http_client_session": self.http_client}
        self.logger = Trace('manageBase')

    @logging("manageBase","login")
    @request(url='/api/manage-base/web/user/login', method='post',headers={"Content-Type":"application/json"})
    def login(self,account,passwd):
        """
        管理中心登录
        """
        params = {"account": account, "passwd": passwd}
        return self.__joinParamKey__(params)

    @logging("manageBase", "logout")
    @request(url='/api/manage-base/web/user/logout', method='post',headers={"Content-Type":"application/json"})
    def logout(self,token):
        """
        管理中心登出
        """
        params = {'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("manageBase", "getUserInfo")
    @request(url='/api/manage-base/web/user/getUserInfo', method='post',headers={"Content-Type":"application/json"})
    def getUserInfo(self,token):
        """
        获取用户信息
        """
        params = {'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("manageBase", "getManagerUserInfo")
    @request(url='/api/manage-base/web/personalCenter/getManagerUserInfo', method='post',headers={"Content-Type":"application/json"})
    def getManagerUserInfo(self,code,phone,token):
        """
        绑定手机号
        """
        params = {"code":code, "phone":phone, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageBase", "getPersonalUserInfo")
    @request(url='/api/manage-base/web/personalCenter/getManagerUserInfo', method='post',headers={"Content-Type":"application/json"})
    def getPersonalUserInfo(self,token):
        """
        获取个人中心基础信息
        """
        params = {'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("manageBase", "getManagerUserInfo")
    @request(url='/api/manage-base/web/user/getManagerUserInfo', method='post',headers={"Content-Type":"application/json"})
    def getManagerUserInfo(self, userId, token):
        """
        获取用户基础信息
        """
        params = {'userId':userId,'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("base", "createUser")
    @request(url='/api/manage-base/web/user/createUser', method='post',headers={"Content-Type": "application/json"})
    def createUser(self, userAccount, userName, userNo, sex, roleId, encryLevelCompany, position, deptIdList,
                   encryLevelDept, token, imgId):
        """
        创建用户
        """
        userDeptPairParamList = [{'deptIdList':deptIdList,'encryLevelDept':encryLevelDept}]
        params = {'name': userName, 'roleId': roleId, 'sex': sex, 'userAccount': userAccount,
                  'userNo': userNo, 'position': position, 'encryLevelCompany': encryLevelCompany,
                  'userDeptPairParamList': userDeptPairParamList, "X-Token": token}
        params = dict(params, **{'imgId': imgId}) if imgId else params
        return self.__joinParamKey__(params)

    @logging("manageBase", "enableOrDisableUser")
    @request(url='/api/manage-base/web/user/enableOrDisableUser', method='post',headers={"Content-Type":"application/json"})
    def enableOrDisableUser(self, userId, status, token):
        """
        启用禁用用户
        """
        params = {'id':userId,'status':status,'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("manageBase", "removeUser")
    @request(url='/api/manage-base/web/user/removeUser', method='post',headers={"Content-Type":"application/json"})
    def removeUser(self, userId, token):
        """
        删除用户
        """
        params = {'data':userId,'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("base", "updateUser")
    @request(url='/api/manage-base/web/user/updateUser', method='post',headers={"Content-Type": "application/json"})
    def updateUser(self, userId, token ,userNo, userName ,sex, roleId, encryLevelCompany):
        """
        查询用户列表
        """
        params = {'id':userId, "X-Token": token}
        params = dict(params, **{'userNo': userNo}) if userNo else params
        params = dict(params, **{'name': userName}) if userName else params
        params = dict(params, **{'sex': sex}) if sex else params
        params = dict(params, **{'roleId': roleId}) if roleId else params
        params = dict(params, **{'encryLevelCompany': encryLevelCompany}) if encryLevelCompany else params
        return self.__joinParamKey__(params)

    @logging("manageBase", "getDeptTree")
    @request(url='/api/manage-base/web/user/getDeptTree', method='post',headers={"Content-Type":"application/json"})
    def getDeptTree(self,token):
        """
        获取组织架构树
        """
        params = {'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("manageBase", "getDictInfo")
    @request(url='/api/manage-base/web/user/getDictInfo', method='post',headers={"Content-Type":"application/json"})
    def getDictInfo(self,key,token):
        """
        获取基础字典值数据
        """
        params = {'key':key,'X-Token': token}
        return self.__joinParamKey__(params)


    @logging("base", "listRoleByPage")
    @request(url='/api/manage-base/web/user/list', method='post',headers={"Content-Type": "application/json"})
    def listUserByPage(self, pageNo, pageSize, token ,status, roleId ,groupParam, deptId):
        """
        查询用户列表
        """
        params = {'pageNo':pageNo,'pageSize':pageSize,"X-Token": token}
        params = dict(params, **{'roleId': roleId}) if roleId else params
        params = dict(params, **{'status': status}) if status else params
        params = dict(params, **{'groupParam': groupParam}) if groupParam else params
        params = dict(params, **{'deptId': deptId}) if deptId else params
        return self.__joinParamKey__(params)

    @logging("manageBase", "getCurrentRoleMenu")
    @request(url='/api/manage-base/web/role/getCurrentRoleMenu', method='post', headers={"Content-Type": "application/json"})
    def getCurrentRoleMenu(self, token):
        """
        获取角色菜单按钮
        """
        params = {"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageBase", "createRole")
    @request(url='/api/manage-base/web/role/create', method='post',headers={"Content-Type": "application/json"})
    def createRole(self, roleName, roleType, roleMenuVOList, roleDesc, token):
        """
        创建角色
        roleType:True 文控 False 普通
        "roleMenuVOList":[{"menuId":1,"permissionFlag":null},{"menuId":2,"permissionFlag":1},{"menuId":3,"permissionFlag":1},{"menuId":9,"permissionFlag":null},{"menuId":10,"permissionFlag":1},{"menuId":11,"permissionFlag":1},{"menuId":12,"permissionFlag":1},{"menuId":13,"permissionFlag":1},{"menuId":14,"permissionFlag":1},{"menuId":15,"permissionFlag":null},{"menuId":16,"permissionFlag":1},{"menuId":17,"permissionFlag":1},{"menuId":18,"permissionFlag":1},{"menuId":19,"permissionFlag":1},{"menuId":20,"permissionFlag":1},{"menuId":21,"permissionFlag":1},{"menuId":22,"permissionFlag":1},{"menuId":23,"permissionFlag":1},{"menuId":24,"permissionFlag":1}]
        """
        # projectMenus = [{'menuId':menuId,'permissionFlag':permissionFlag} for menuId in roleMenuVOList]
        # projectMenus = [{'menuId':menuId,'readonly':readonly,'projectId':0} for menuId in projectMenuIds]
        params = {"roleName": roleName, "roleType":roleType,"roleMenuVOList":roleMenuVOList,"roleDesc":roleDesc,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageBase", "updateRoleStatus")
    @request(url='/api/manage-base/web/role/updateStatus', method='post',headers={"Content-Type": "application/json"})
    def updateRoleStatus(self, roleId, roleStatus, token):
        """
        禁用、启用角色
        """
        params = {"id":roleId,"roleStatus": roleStatus, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageBase", "updateRole")
    @request(url='/api/manage-base/web/role/update', method='post',headers={"Content-Type": "application/json"})
    def updateRole(self, roleId, roleName, roleMenuVOList, roleDesc, roleType, token):
        """
        更新角色
        """
        params = {"id": roleId, "roleName": roleName, "roleMenuVOList": roleMenuVOList, "roleDesc": roleDesc,
                  "roleType": roleType, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageBase", "getBaseMenu")
    @request(url='/api/manage-base/web/role/getBaseMenu', method='post',headers={"Content-Type": "application/json"})
    def getBaseMenu(self, code, level, token):
        """
        获取角色菜单权限
        """
        params = {"code": code, "level": level, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("base", "listRoleByPage")
    @request(url='/api/manage-base/web/role/listByPage', method='post',headers={"Content-Type": "application/json"})
    def listRoleByPage(self, pageNo, pageSize, token ,status, searchValue):
        """
        查询角色列表
        """
        params = {'pageNo':pageNo,'pageSize':pageSize,"X-Token": token}
        params = dict(params, **{'searchValue': searchValue}) if searchValue else params
        params = dict(params, **{'status': status}) if status else params
        return self.__joinParamKey__(params)

    @logging("manageBase", "getPhoneCode")
    @request(url='/api/manage-base/web/user/getPhoneCode', method='post',headers={"Content-Type": "application/json"})
    def getPhoneCode(self, phone, token):
        """
        获取手机验证码
        :param phone:
        :param token:
        :return:
        """
        params = {'data': phone, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("manageBase", "verifyPhoneCode")
    @request(url='/api/manage-base/web/user/verifyPhoneCode', method='post',headers={"Content-Type": "application/json"})
    def verifyPhoneCode(self, phone, code, token):
        """
        校验手机验证码
        :param phone:
        :param code:
        :return:
        """
        params = {'phone':phone,'code': code, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("manageBase", "updatePhone")
    @request(url='/api/manage-base/web/user/bindPhone', method='post',headers={"Content-Type":"application/json"})
    def bindPhone(self,code,phone,token):
        """
        绑定手机号
        """
        params = {"code":code, "phone":phone, "X-Token": token}
        return self.__joinParamKey__(params)



    @logging("manageBase", "resetUserPassword")
    @request(url='/api/manage-base/web/user/resetPassword', method='post',headers={"Content-Type": "application/json"})
    def resetUserPassword(self, account, passwd, code, token):
        """
        重置自己密码
        """
        params = {'account': account, 'passwd':passwd, 'code':code, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("manageBase", "__joinParamKey__")
    def __joinParamKey__(self, params,method = 'post',**kwargs):
        """
        :param params:
        :param method:
        :param kwargs:
        :return:
        """
        # 将request body转换成json
        # params = json.dumps(params, ensure_ascii=False)
        params = dict({'params': params}, **kwargs) if method is 'GET' else {'data': params}
        return dict(params, **self.common_params)
