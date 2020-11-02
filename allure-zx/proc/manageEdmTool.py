#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on July 15, 2019
@author: hzhuangfg
'''
from business.manageEdm import *
from check.checkManageBase import CheckResult
from com.api import logging
from com.util import gen_md5_sign
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式

class manageEdmTool():
    def __init__(self,logId,env='test',http_client=None):
        self.env = env
        self.logId = gen_md5_sign(logId)
        self.projectId = 'hoolink'
        self.manageedm = manageEdm(self.logId,self.env,http_client)
        self.checker = CheckResult(self.logId,self.env,http_client)
        self.http_client = http_client
        self.logger = Trace('manageEdmTool')

    @logging("manageEdmTool", "logout")
    def getInitDeptResourceMenu(self,token):
        """
        获得部门资源列表
        """
        resp = self.manageedm.getInitDeptResourceMenu(token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "getInitResourceMenu")
    def getInitResourceMenu(self,token):
        """
        初始化我的收藏资源列表树结构
        """
        resp = self.manageedm.getInitResourceMenu(token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "getInitCompanyResourceMenu")
    def getInitCompanyResourceMenu(self, token):
        """
        获得资源库列表
        """
        resp = self.manageedm.getInitCompanyResourceMenu(token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "getInitCacheResourceMenu")
    def getInitCacheResourceMenu(self, token):
        """
        获得缓冲库资源列表
        """
        resp = self.manageedm.getInitCacheResourceMenu(token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "bindPhone")
    def getFreshenMenu(self, belongId, repertoryType, token, id):
        """
        获得刷新菜单
        """
        resp = self.manageedm.getFreshenMenu(belongId, repertoryType, token, id).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp


    @logging("manageEdmTool", "resetUserPassword")
    def getNavBar(self, belongId, repertoryType, token, id):
        """
        获得导航栏
        """
        resp = self.manageedm.getNavBar(belongId, repertoryType, token, id).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "getCurrentRoleMenu")
    def downLoadFile(self, fileId, repertoryType, token):
        """
        下载文件
        """
        resp = self.manageedm.downLoadFile(fileId, repertoryType, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "downLoadFileToZip")
    def downLoadFileToZip(self,fileIds, repertoryType, token):
        """
        打包下载文件
        """
        resp = self.manageedm.downLoadFileToZip(fileIds, repertoryType, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "fileOutput")
    def fileOutput(self,fileIds, description, token):
        """
        输出文件到缓存库
        """
        resp = self.manageedm.fileOutput(fileIds, description, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "readFilesByParam")
    def readFilesByParam(self,departmentId, fileNameSort, fileSizeSort, fileTypeSort, isMostJunior, menuType, repertoryTypeCode,
                         createTimeSort, fileName, pageNo, pageSize, token, directoryId):
        """
        检索当前目录及其下级目录中的文件
        """
        resp = self.manageedm.readFilesByParam(departmentId, fileNameSort, fileSizeSort, fileTypeSort, isMostJunior, menuType, repertoryTypeCode,
                         createTimeSort, fileName, pageNo, pageSize, token, directoryId).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "fileRemove")
    def fileRemove(self, idList, repertoryType, token):
        """
        删除文件
        """
        resp = self.manageedm.fileRemove(idList, repertoryType, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "addCollection")
    def addCollection(self,collectionResourceBOS, repertoryType, parentId, token):
        """
        添加收藏
        """
        resp = self.manageedm.addCollection(collectionResourceBOS, repertoryType, parentId, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "removeCollection")
    def removeCollection(self, batchInsertOperateRecordBOS, repertoryType, token):
        """
        取消收藏
        """
        resp = self.manageedm.removeCollection(batchInsertOperateRecordBOS, repertoryType, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "getDeptTree")
    def getOrgTree(self, deptId, deptType, repertoryType, resourceList, token):
        """
        文件权限设置的组织架构树
        """
        resp = self.manageedm.getOrgTree(deptId, deptType, repertoryType, resourceList, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "setFilePermissions")
    def setFilePermissions(self,deptIdList, repertoryType, securityLevel, token, deptRepertoryParamList, companyRepertoryParamList):
        """
        文件权限设置
        """
        resp = self.manageedm.setFilePermissions(deptIdList, repertoryType, securityLevel, token, deptRepertoryParamList, companyRepertoryParamList).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "deleteVisibleOrg")
    def deleteVisibleOrg(self, deptId, isLastOne, orgId, repertoryType, resourceId, token):
        """
        删除可见组织
        """
        resp = self.manageedm.deleteVisibleOrg(deptId, isLastOne, orgId, repertoryType, resourceId, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "createUser")
    def readCollectionFilesByParam(self, directoryId, fileNameSort, fileSizeSort, fileTypeSort, repertoryTypeCode,
                                   createTimeSort, fileName, pageNo, pageSize, token):
        """
        查询收藏列表
        """
        resp = self.manageedm.readCollectionFilesByParam(directoryId, fileNameSort, fileSizeSort, fileTypeSort,
                                                         repertoryTypeCode, createTimeSort, fileName, pageNo, pageSize,
                                                         token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "getNextResourceMenu")
    def getNextResourceMenu(self,repertoryType, token, id, belongId):
        """
        获得下一级权限资源列表
        """
        resp = self.manageedm.getNextResourceMenu(repertoryType, token, id, belongId).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "selectTreeToOrg")
    def selectTreeToOrg(self,orgId, repertoryType, resourceInfoList, token):
        """
        目录选择树--组织架构
        """
        resp = self.manageedm.selectTreeToOrg(orgId, repertoryType, resourceInfoList, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "selectTreeToFile")
    def selectTreeToFile(self,orgId, repertoryType, token):
        """
        目录选择树--文件或文件夹
        """
        resp = self.manageedm.selectTreeToFile(orgId, repertoryType, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "fileMove")
    def fileMove(self,aimsOrgId, aimsParentIdCode, aimsResourceId, repertoryType, resourceInfoList, token):
        """
        移动文件
        """
        resp = self.manageedm.fileMove(aimsOrgId, aimsParentIdCode, aimsResourceId, repertoryType, resourceInfoList, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "getMaintainInitMenu")
    def getMaintainInitMenu(self,repertoryType, level, token, id, belongId):
        """
        获取维护文档菜单
        """
        resp = self.manageedm.getMaintainInitMenu(repertoryType, level, token, id, belongId).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "maintain")
    def maintain(self,departmentId, repertoryType, resourceList, token, parentId):
        """
        维护文档目录接口
        """
        resp = self.manageedm.maintain(departmentId, repertoryType, resourceList, token, parentId).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "visibleTree")
    def visibleTree(self,flag, token):
        """
        临时权限设置页面树形结构
        """
        resp = self.manageedm.visibleTree(flag, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "visibleCreate")
    def visibleCreate(self,userIdList, repertoryList, expireTime, reason, token):
        """
        设置资源临时权限
        """
        resp = self.manageedm.visibleCreate(userIdList, repertoryList, expireTime, reason, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "visibleCreate")
    def previewContent(self,repertoryType, resourceId, token):
        """
        文件预览
        """
        resp = self.manageedm.previewContent(repertoryType, resourceId, token).json
        resp.checker = self.__dealwithCommResp__(resp)
        return resp

    @logging("manageEdmTool", "__dealwithCommResp__")
    def __dealwithCommResp__(self,resp):
        """
        :param resp:
        :return:
        """
        if resp is not None and resp.has_key('data'):
            if resp.status is True:
                return True
        return False

    @logging("manageEdmTool", "__dealwithLocustResp__")
    def __dealwithLocustResp__(self,resp):
        """
        :param resp:
        :return:
        """
        if resp is not None:
            if resp.status is True and self.http_client is not None:
                return True
        return False

