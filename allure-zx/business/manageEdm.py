#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
Created on July 03, 2019
@author: hzhuangfg
'''
import json
from Config import get_manage_url
from com.util import *
from com.Lib import *
from engine.runner import Runner
from com.api import request,logging

class manageEdm(object):

    def __init__(self, logId, env='test', http_client=None):
        self.appid = self.logId = logId
        self.base_url = get_manage_url(env)
        self.http_client = http_client
        self.runner = Runner(http_client)
        self.common_params = {"http_client_session": self.http_client}
        self.logger = Trace('manageEdm')


    @logging("manageEdm", "commonUploadFile")
    @request(url='/api/manage-edm/web/file/commonUploadFile', method='post',headers={"Content-Type":"application/json"})
    def commonUploadFile(self, backupObsId, deptId, fileAllPath, fileSize, obsId, parentId, repertoryType,
                         securityLevel, labelNameList, permissionDeptIdList, token):
        """
        上传文件
        """
        params = {'backupObsId': backupObsId, 'deptId': deptId, 'fileAllPath': fileAllPath, 'fileSize': fileSize,
                  'obsId': obsId, 'parentId': parentId, 'repertoryType': repertoryType, 'securityLevel': securityLevel,
                  'labelNameList': labelNameList, 'permissionDeptIdList': permissionDeptIdList, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "readFilesByParam")
    @request(url='/api/manage-edm/web/fileDirectory/readFilesByParam', method='post',headers={"Content-Type":"application/json"})
    def readFilesByParam(self, departmentId, fileNameSort, fileSizeSort, fileTypeSort, isMostJunior, menuType, repertoryTypeCode,
                         createTimeSort, fileName, pageNo, pageSize, token, directoryId):
        """
        :param departmentId:部门id
        :param menuType:是否组织架构，自定义目录传False
        :param fileTypeSort:（选填）资源类行排序（1.升序 2.降序）
        :param isMostJunior:是否最下级组织架构
        :param repertoryTypeCode:资源类型（1.部门资源 2.缓存资源 3.资源库）
        :param directoryId:目录id
        检索当前目录及其下级目录中的文件
        """
        params = {'departmentId': departmentId, 'fileNameSort': fileNameSort, 'fileSizeSort': fileSizeSort, 'fileTypeSort': fileTypeSort,
                  'isMostJunior': isMostJunior, 'menuType': menuType, 'repertoryTypeCode': repertoryTypeCode, 'createTimeSort': createTimeSort,
                  'fileName': fileName, 'pageNo': pageNo, 'pageSize': pageSize, 'X-Token': token}
        params = dict(params, **{'directoryId': directoryId}) if directoryId else params
        return self.__joinParamKey__(params)


    @logging("manageEdm", "getInitDeptResourceMenu")
    @request(url='/api/manage-edm/web/deptResource/getInitDeptResourceMenu', method='post',headers={"Content-Type": "application/json"})
    def getInitDeptResourceMenu(self, token):
        """
        获得部门资源列表
        """
        params = {"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "getInitResourceMenu")
    @request(url='/api/manage-edm/web/fileDirectory/getInitResourceMenu', method='post',headers={"Content-Type": "application/json"})
    def getInitResourceMenu(self, token):
        """
        初始化我的收藏资源列表树结构
        """
        params = {"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "getInitResourceMenu")
    @request(url='/api/manage-edm/web/deptResource/getInitCompanyResourceMenu', method='post',headers={"Content-Type": "application/json"})
    def getInitCompanyResourceMenu(self, token):
        """
        获得资源库列表
        """
        params = {"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "getInitCacheResourceMenu")
    @request(url='/api/manage-edm/web/deptResource/getInitCacheResourceMenu', method='post',headers={"Content-Type": "application/json"})
    def getInitCacheResourceMenu(self, token):
        """
        获得缓冲库资源列表
        """
        params = {"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "getFreshenMenu")
    @request(url='/api/manage-edm/web/deptResource/getFreshenMenu', method='post',headers={"Content-Type": "application/json"})
    def getFreshenMenu(self, belongId, repertoryType, token, id):
        """
        获得刷新菜单
        :param belongId:组织架构id
        :param repertoryType:库类别 1：部门资源 2：缓存库资源 3：资源库 4：公共资源
        :param id:资源id[与belongId只传其一]
        :param token:
        :return:
        """
        params = {'belongId':belongId,'repertoryType':repertoryType,"X-Token": token}
        params = dict(params, **{'id': id}) if id else params
        return self.__joinParamKey__(params)

    @logging("manageEdm", "getNextResourceMenu")
    @request(url='/api/manage-edm/web/deptResource/getNextResourceMenu', method='post',headers={"Content-Type": "application/json"})
    def getNextResourceMenu(self, repertoryType, token, id, belongId):
        """
        获得下一级权限资源列表
        :param belongId:归属部门|小组id（菜单id）【部门库专属使用】
        :param repertoryType:库类别 1：部门资源 2：缓存库资源 3：资源库 4：公共资源
        :param id:资源id（菜单id）[与belongId只传其一]
        :param token:
        :return:
        """
        params = {'repertoryType': repertoryType, "X-Token": token}
        params = dict(params, **{'id': id}) if id else params
        params = dict(params, **{'belongId': belongId}) if belongId else params
        return self.__joinParamKey__(params)

    @logging("manageEdm", "getNavBar")
    @request(url='/api/manage-edm/web/deptResource/getNavBar', method='post',headers={"Content-Type": "application/json"})
    def getNavBar(self, belongId, repertoryType, token, id):
        """
        获得导航栏
        :param belongId:组织架构id
        :param repertoryType:库类别 1：部门资源 2：缓存库资源 3：资源库 4：公共资源
        :param id:资源id[与belongId只传其一]
        :param token:
        :return:
        """
        params = {'belongId':belongId,'repertoryType':repertoryType,"X-Token": token}
        params = dict(params, **{'id': id}) if id else params
        return self.__joinParamKey__(params)

    @logging("manageEdm", "downLoadFile")
    @request(url='/api/manage-edm/web/download/downLoadFile', method='post',headers={"Content-Type": "application/json"})
    def downLoadFile(self, fileId, repertoryType, token):
        """
        下载文件
        :param fileId:文件id
        :param repertoryType:库类别 1：部门资源 2：缓存库资源 3：资源库 4：公共资源
        :param token:
        :return:
        """
        params = {'fileId':fileId,'repertoryType':repertoryType,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "downLoadFileToZip")
    @request(url='/api/manage-edm/web/download/downLoadFileToZip', method='post',headers={"Content-Type": "application/json"})
    def downLoadFileToZip(self, fileIds, repertoryType, token):
        """
        下载文件
        :param fileIds:["edm_2266", "edm_1222", "edm_2265"]
        :param repertoryType:库类别 1：部门资源 2：缓存库资源 3：资源库 4：公共资源
        :param token:
        :return:
        """
        params = {'fileIds':fileIds,'repertoryType':repertoryType,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "fileOutput")
    @request(url='/api/manage-edm/web/deptResource/fileOutput', method='post',headers={"Content-Type": "application/json"})
    def fileOutput(self, fileIds, description, token):
        """
        输出文件到缓存库
        :param fileIds:["edm_2266", "edm_1222", "edm_2265"]
        :param description:
        :param token:
        :return:
        """
        params = {'fileIds':fileIds,'description':description,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "fileRemove")
    @request(url='/api/manage-edm/web/file/fileRemove', method='post',headers={"Content-Type": "application/json"})
    def fileRemove(self, idList, repertoryType, token):
        """
        删除文件
        :param idList:文件或者文件夹当前id:["edm_2266", "edm_1222", "edm_2265"]
        :param repertoryType:库类别 1：部门资源 2：缓存库资源 3：资源库 4：公共资源
        :param token:
        :return:
        """
        params = {'idList':idList,'repertoryType':repertoryType,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "addCollection")
    @request(url='/api/manage-edm/web/fileDirectory/addCollection', method='post',headers={"Content-Type": "application/json"})
    def addCollection(self, collectionResourceBOS, repertoryType, parentId, token):
        """
        添加收藏
        :param collectionResourceBOS:{isFolder: false, id: "edm_1222", fileSuffix: "txt", obsId: 1380, resourceName: "nginx.txt"}
        :param repertoryType:库类别 1：部门资源 2：缓存库资源 3：资源库 4：公共资源
        :param parentId:
        :param token:
        :return:
        """
        params = {'collectionResourceBOS':collectionResourceBOS,'repertoryType':repertoryType,"X-Token": token, 'parentId': parentId}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "removeCollection")
    @request(url='/api/manage-edm/web/fileDirectory/removeCollection', method='post',headers={"Content-Type": "application/json"})
    def removeCollection(self, batchInsertOperateRecordBOS, repertoryType, token):
        """
        取消收藏
        :param batchInsertOperateRecordBOS:[{"id":"edm_2357","obsId":2949,"fileSuffix":"jpg","resourceName":"顾梦珂.jpg"}]
        :param repertoryType:库类别 1：部门资源 2：缓存库资源 3：资源库 4：公共资源
        :param token:
        :return:
        """
        params = {'batchInsertOperateRecordBOS':batchInsertOperateRecordBOS,'repertoryType':repertoryType,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "getOrgTree")
    @request(url='/api/manage-edm/web/permissionSettings/getOrgTree', method='post',headers={"Content-Type": "application/json"})
    def getOrgTree(self, deptId, deptType, repertoryType, resourceList, token):
        """
        文件权限设置的组织架构树
        :param resourceList:[{"resourceId":"edm_800","resourceType":true,"securityLevel":0},{"resourceId":"edm_814","resourceType":false,"securityLevel":2}]
        :param deptType:层级参数 1-公司 2-部门 3-小组
        :param deptId:文件所在公司的id --> deptId: 78
        :param token:
        :return:
        """
        params = {'deptId':deptId,'deptType':deptType,'repertoryType':repertoryType, 'resourceList':resourceList, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "selectTreeToOrg")
    @request(url='/api/manage-edm/web/fileMove/selectTreeToOrg', method='post',headers={"Content-Type": "application/json"})
    def selectTreeToOrg(self, orgId, repertoryType, resourceInfoList, token):
        """
        目录选择树--组织架构
        :param resourceInfoList:[{parentIdCode: "0_2160_2585_", resourceId: "edm_2585", fileType: false}]
        :param repertoryType:库类别 1：部门资源 2：缓存库资源 3：资源库 4：公共资源
        :param token:
        :return:
        """
        params = {'orgId':orgId,'repertoryType':repertoryType, 'resourceInfoList':resourceInfoList, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "selectTreeToFile")
    @request(url='/api/manage-edm/web/fileMove/selectTreeToFile', method='post',headers={"Content-Type": "application/json"})
    def selectTreeToFile(self, orgId, repertoryType, token):
        """
        目录选择树--文件或文件夹
        :param orgId: 组织id
        :param repertoryType:库类别 1：部门资源 2：缓存库资源 3：资源库 4：公共资源
        :param token:
        :return:
        """
        params = {'orgId': orgId, 'repertoryType': repertoryType, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "fileMove")
    @request(url='/api/manage-edm/web/fileMove/move', method='post',headers={"Content-Type": "application/json"})
    def fileMove(self, aimsOrgId, aimsParentIdCode, aimsResourceId, repertoryType, resourceInfoList, token):
        """
        移动文件
        :param resourceInfoList:[{fileSuffix: "jpg", fileType: 0, obsId: 3111, orgId: "dept_78", parentId: "edm_2160",parentIdCode: "0_2160_2585_",resourceId: "edm_2585",resourceName: "东立2.jpg"}]
        :param repertoryType:库类别 1：部门资源 2：缓存库资源 3：资源库 4：公共资源
        :param aimsOrgId:目标文件夹资源的department_id（目录所选的文件夹id）必填
        :param aimsParentIdCode:目标文件夹中的父节点层级code（目录所选的文件夹id）
        :param aimsResourceId:目标文件夹资源id（目录所选的文件夹id,如果移动到的是组织架构下就传0）（必填）
        :param repertoryType:资源类型:1部门资源，2缓存库，3资源库
        :param fileType:文件 0 | 文件夹 1
        :param orgId:资源中的组织架构id（department_id）
        :param parentId:资源中的上级目录id
        :param parentIdCode:资源中的父节点层级code
        :param resourceId:资源id
        :param resourceName:资源名称
        :param token:
        :return:
        """
        params = {'aimsOrgId': aimsOrgId, 'aimsParentIdCode': aimsParentIdCode, 'aimsResourceId': aimsResourceId,
                  'repertoryType': repertoryType, 'resourceInfoList': resourceInfoList, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "getMaintainInitMenu")
    @request(url='/api/manage-edm/web/maintain/getMaintainInitMenu', method='post',headers={"Content-Type": "application/json"})
    def getMaintainInitMenu(self, repertoryType, level, token, id, belongId):
        """
        获取维护文档菜单
        :param level:初始化几级目录（不传或0默认3级）
        :param repertoryType:库类别 1：部门资源 2：缓存库资源 3：资源库 4：公共资源
        :param id:操作文件夹id
        :param belongId:所属直接上级组织架构（只有部门库和资源库会用到 ；和id只传其一，视情况而定）
        :return:
        """
        params = {'level':level,'repertoryType':repertoryType, "X-Token": token}
        params = dict(params, **{'belongId': id}) if id else params
        params = dict(params, **{'belongId': belongId}) if belongId else params
        return self.__joinParamKey__(params)

    @logging("manageEdm", "maintain")
    @request(url='/api/manage-edm/web/maintain/maintain', method='post',headers={"Content-Type": "application/json"})
    def maintain(self, departmentId, repertoryType, resourceList, token, parentId):
        """
        维护文档目录接口
        :param departmentId:（必传）最内层组织架构id
        :param parentId:直接父级id（不算组织架构）
        :param repertoryType:库类别 1：部门资源 2：缓存库资源 3：资源库 4：公共资源
        :param resourceList:直接父级id（不算组织架构）  [{id: "", resourceName: "test001"}] resourceId:资源id （为0或空表是新增 大于0代表修改）,resourceName:资源名称
        :param token:
        :return:
        """
        params = {'departmentId': departmentId, 'repertoryType': repertoryType, 'resourceList': resourceList,
                  "X-Token": token}
        params = dict(params, **{'parentId': parentId}) if parentId else params
        return self.__joinParamKey__(params)

    @logging("manageEdm", "setFilePermissions")
    @request(url='/api/manage-edm/web/permissionSettings/setFilePermissions', method='post',headers={"Content-Type": "application/json"})
    def setFilePermissions(self, deptIdList, repertoryType, securityLevel, token, deptRepertoryParamList, companyRepertoryParamList):
        """
        文件权限设置
        :param deptRepertoryParamList:[{fileSuffix: "jpg", id: "edm_2585", obsId: 3111, parentIdCode: "0_2737_2585_", resourceName: "东立2.jpg",…}]  部门资源库
        :param companyRepertoryParamList:[{"fileSuffix":"jpg","id":"edm_1099","obsId":3335,"parentIdCode":"0_1088_1099_","resourceName":"1 - 副本.jpg","resourceType":false}] 资源库
        :param deptIdList:[48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,20,21,22,23,72,73,74,75,76,77,26,27,28,29,78,79,80,31,32,81,82,83,84,85,86,35,36,37,38,39,40,41]
        :param token:
        :return:
        """
        params = { 'deptIdList': deptIdList, 'repertoryType': repertoryType, 'securityLevel': securityLevel, "X-Token": token}
        params = dict(params, **{'deptRepertoryParamList': deptRepertoryParamList}) if deptRepertoryParamList else params
        params = dict(params, **{'companyRepertoryParamList': companyRepertoryParamList}) if companyRepertoryParamList else params
        return self.__joinParamKey__(params)


    @logging("manageEdm", "deleteVisibleOrg")
    @request(url='/api/manage-edm/web/permissionSettings/deleteVisibleOrg', method='post',headers={"Content-Type": "application/json"})
    def deleteVisibleOrg(self, deptId, isLastOne, orgId, repertoryType, resourceId, token):
        """
        删除可见组织
        {"orgId":45,"deptId":1,"repertoryType":3,"resourceId":"edm_1057","isLastOne":false}
        :param deptId:文件所在公司的id
        :param isLastOne:文件是否是最后一个可见组织架构 true：是最后一个；false：否
        :param orgId:(必填)组织架构id(可见组织架构id)
        :param repertoryType:(必填)资源类型（1：部门资源 2：缓存库资源 3：资源库 4：公共资源）
        :param resourceId:(必传）资源id
        :return:
        """
        params = {'deptId': deptId, 'isLastOne': isLastOne, 'orgId': orgId, 'repertoryType': repertoryType,
                  'resourceId': resourceId, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "visibleTree")
    @request(url='/api/manage-edm/web/repertory/visible/tree', method='post',headers={"Content-Type": "application/json"})
    def visibleTree(self, flag, token):
        """
        临时权限设置页面树形结构
        :param resourceList:true 查询架构下人员 false：不查询
        :param token:
        :return:
        """
        params = {'data':flag, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "visibleCreate")
    @request(url='/api/manage-edm/web/repertory/visible/create', method='post',headers={"Content-Type": "application/json"})
    def visibleCreate(self, userIdList, repertoryList, expireTime, reason, token):
        """
        设置资源临时权限
        :param userIdList:[369]
        :param repertoryList:[{id: "edm_797", repertoryIdCode: "0_797_", resourceType: false}]
        :param expireTime:2019-07-12 00:00:00
        :return:
        """
        params = {'userIdList': userIdList, 'repertoryList': repertoryList, 'expireTime': expireTime, 'reason': reason,
                  "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "previewContent")
    @request(url='/api/manage-edm/web/file/previewContent', method='post',headers={"Content-Type": "application/json"})
    def previewContent(self, repertoryType, resourceId, token):
        """
        文件预览
        :param repertoryType:1：部门资源 2：缓存库资源 3：资源库 4：公共资源
        :param resourceId:资源id
        :return:
        """
        params = {'repertoryType': repertoryType, 'resourceId': resourceId, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "readCollectionFilesByParam")
    @request(url='/api/manage-edm/web/fileDirectory/readCollectionFilesByParam', method='post',headers={"Content-Type":"application/json"})
    def readCollectionFilesByParam(self, directoryId, fileNameSort, fileSizeSort, fileTypeSort, repertoryTypeCode,createTimeSort, fileName, pageNo, pageSize, token):
        """
        查询收藏列表
        :param fileTypeSort:（选填）资源类行排序（1.升序 2.降序）
        :param repertoryTypeCode:资源类型（1.部门资源 2.缓存资源 3.资源库）
        :param directoryId:目录id
        """
        params = {'directoryId': directoryId, 'fileNameSort': fileNameSort, 'fileSizeSort': fileSizeSort, 'fileTypeSort': fileTypeSort,
                   'repertoryTypeCode': repertoryTypeCode, 'createTimeSort': createTimeSort,
                  'fileName': fileName, 'pageNo': pageNo, 'pageSize': pageSize, 'X-Token': token}
        return self.__joinParamKey__(params)

    @logging("manageEdm", "__joinParamKey__")
    def __joinParamKey__(self, params,method = 'post',**kwargs):
        """
        :param params:
        :param method:
        :param kwargs:
        :return:
        """
        params = dict({'params': params}, **kwargs) if method is 'GET' else {'data': params}
        return dict(params, **self.common_params)
