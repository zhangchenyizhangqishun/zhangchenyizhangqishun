#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on July 12, 2019
@author: hzhuangfg
'''
from smokeUtils import *
from com.util import gen_random_target
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式

def getInitDeptResourceMenu(token,title):
    with pytest.allure.step("获得部门资源列表 token={0}，title={1}".format(token,title)):
        return manageEdmTool.getInitDeptResourceMenu(token)

def getInitResourceMenu(token, title):
    with pytest.allure.step("初始化我的收藏资源列表树结构 token={0}，title={1}".format(token,title)):
        return manageEdmTool.getInitResourceMenu(token)
        # assert check_value(resp.checker, True)
        # return next(resp('$..*[@.title is "%s"].key' % title))  # key: "edm_-1"

def getInitCacheResourceMenu(token,title):
    with pytest.allure.step("获得缓冲库资源列表 token={0}，title={1}".format(token,title)):
        return manageEdmTool.getInitCacheResourceMenu(token)

def getInitCompanyResourceMenu(token):
    with pytest.allure.step("获得资源库列表 token={0}".format(token)):
        return manageEdmTool.getInitCompanyResourceMenu(token)
        # assert check_value(resp.checker, True)
        # return resp

def getFreshenMenu(belongId, repertoryType, token, id):
    with pytest.allure.step("获得刷新菜单 belongId={0}，id={1}，repertoryType={2}".format(belongId, id, repertoryType)):
        return manageEdmTool.getFreshenMenu(belongId, repertoryType, token, id)

def getNavBar(belongId, repertoryType, token, id):
    with pytest.allure.step("获得导航栏 belongId={0}，id={1}，repertoryType={2}".format(belongId, id, repertoryType)):
        return manageEdmTool.getNavBar(belongId, repertoryType, token, id)

def downLoadFile(fileId, repertoryType, token):
    with pytest.allure.step("下载文件 fileId={0}，repertoryType={1}".format(fileId, repertoryType)):
        resp = manageEdmTool.downLoadFile(fileId, repertoryType, token)
        # assert check_value(resp.message, message)
        # assert check_value(resp.checker, True)
        return resp

def downLoadFileToZip(fileIds, repertoryType, token):
    with pytest.allure.step("打包下载文件 fileIds={0}，repertoryType={1}".format(fileIds,repertoryType)):
        resp = manageEdmTool.downLoadFileToZip(fileIds, repertoryType, token)
        assert check_value(resp.checker, True)
        return resp

def readFilesByParam(departmentId, isMostJunior, menuType, repertoryTypeCode, token, directoryId='', fileName=None):
    # 查询组织架构不需要传directoryId，如果是自定义目录需要传directoryId -->"edm_2160"
    with pytest.allure.step(
            "检索当前目录及其下级目录中的文件 departmentId={0}，isMostJunior={1}，menuType={2}，repertoryTypeCode={3}，directoryId={4}，fileName={5}".format(
                departmentId,
                isMostJunior,
                menuType,
                repertoryTypeCode,
                directoryId,
                fileName)):
        pageNo = 1
        pageSize = 200
        fileNameSort = 1
        fileSizeSort = 0
        fileTypeSort = 0
        createTimeSort = 0
        resp = manageEdmTool.readFilesByParam(departmentId, fileNameSort, fileSizeSort, fileTypeSort, isMostJunior, menuType, repertoryTypeCode,
                         createTimeSort, fileName, pageNo, pageSize, token, directoryId)
        assert check_value(resp.checker, True)
        return resp

def fileOutput(fileIds, token):
    description = gen_random_target()
    with pytest.allure.step("输出文件到缓存库 fileIds={0}，description={1}".format(fileIds,description)):
        return manageEdmTool.fileOutput(fileIds, description, token)

def addCollection(collectionResourceBOS, repertoryType, parentId, token):
    with pytest.allure.step("添加收藏 collectionResourceBOS={0}，repertoryType={1}".format(collectionResourceBOS,repertoryType)):
        return manageEdmTool.addCollection(collectionResourceBOS, repertoryType, parentId, token)

def removeCollection(batchInsertOperateRecordBOS, repertoryType, token):
    with pytest.allure.step("取消收藏 collectionResourceBOS={0}，repertoryType={1}".format(batchInsertOperateRecordBOS,repertoryType)):
        return manageEdmTool.removeCollection(batchInsertOperateRecordBOS, repertoryType, token)

def readCollectionFilesByParam(directoryId, repertoryTypeCode, fileName, token):
    with pytest.allure.step("查询收藏列表 directoryId={0}，repertoryTypeCode={1}，fileName={2}".format(directoryId,repertoryTypeCode,fileName)):
        pageNo = 1
        pageSize = 20
        fileNameSort = 1
        fileSizeSort = 0
        fileTypeSort = 0
        createTimeSort = 0
        return manageEdmTool.readCollectionFilesByParam(directoryId, fileNameSort, fileSizeSort, fileTypeSort, repertoryTypeCode,
                                   createTimeSort, fileName, pageNo, pageSize, token)

def getNextResourceMenu(repertoryType, token, id, belongId):
    with pytest.allure.step("获得下一级权限资源列表 id={0}，repertoryType={1}，belongId={2}".format(id,repertoryType,belongId)):
        return manageEdmTool.getNextResourceMenu(repertoryType, token, id, belongId)

def selectTreeToOrg(orgId, repertoryType, fileinfo, token, message):
    resourceInfoList = [{'parentIdCode': fileinfo.parentIdCode, 'resourceId': fileinfo.id, 'fileType': fileinfo.fileType}]
    with pytest.allure.step("目录选择树--组织架构 orgId={0}，repertoryType={1}，resourceInfoList={2}".format(orgId,repertoryType,resourceInfoList)):
        resp = manageEdmTool.selectTreeToOrg(orgId, repertoryType, resourceInfoList, token)
        assert check_value(resp.message, message)

def selectTreeToFile(orgId, repertoryType, token):
    with pytest.allure.step("目录选择树--文件或文件夹 orgId={0}，repertoryType={1}".format(orgId,repertoryType)):
        return manageEdmTool.selectTreeToFile(orgId, repertoryType, token)

def fileMove(aimsOrgId, aimsParentIdCode, aimsResourceId, repertoryType, resourceInfoList, token):
    with pytest.allure.step(
            "移动文件 aimsOrgId={0}，aimsParentIdCode={1}，aimsResourceId={2}，repertoryType={3}，resourceInfoList={4}".format(
                    aimsOrgId, aimsParentIdCode, aimsResourceId, repertoryType, resourceInfoList)):
        return manageEdmTool.fileMove(aimsOrgId, aimsParentIdCode, aimsResourceId, repertoryType, resourceInfoList, token)

def getMaintainInitMenu(repertoryType, level, token, id, belongId):
    with pytest.allure.step(
            "获取维护文档菜单 level={0}，repertoryType={1}，id={2}，belongId={3}".format(level, repertoryType, id, belongId)):
        return manageEdmTool.getMaintainInitMenu(repertoryType, level, token, id, belongId)

def maintain(departmentId, repertoryType, resourceList, token, parentId=''):
    with pytest.allure.step(
            "维护文档目录 departmentId={0}，repertoryType={1}，parentId={2}，resourceList={3}".format(departmentId,
                                                                                             repertoryType,
                                                                                             parentId,
                                                                                             resourceList)):
        return manageEdmTool.maintain(departmentId, repertoryType, resourceList, token, parentId)

def fileRemove(idList, repertoryType, token):
    with pytest.allure.step("删除文件 idList={0}，repertoryType={1}".format(idList,repertoryType)):
        return manageEdmTool.fileRemove(idList, repertoryType, token)

def getOrgTree(deptId, deptType, repertoryType, resourceList, token):
    with pytest.allure.step(
            "组织架构树-文件权限设置 deptId={0}，deptType={1}，repertoryType={2}，resourceList={3}".format(deptId, deptType,
                                                                                             repertoryType,
                                                                                             resourceList)):
        return manageEdmTool.getOrgTree(deptId, deptType, repertoryType, resourceList, token)

def setFilePermissions(deptId, deptType, fileinfo, repertoryType, securityLevel, token, message, deptTitles=[]):
    RepertoryParamList = [{'id': fileinfo.id, 'fileSuffix': fileinfo.fileSuffix, 'obsId': fileinfo.obsId,
                                  'resourceName': fileinfo.resourceName, 'parentIdCode': fileinfo.parentIdCode,
                                  'resourceType': fileinfo.resourceType}]
    resourceList = [
        {'resourceId': fileinfo.id, 'resourceType': fileinfo.resourceType, 'securityLevel': fileinfo.securityLevel}]
    resp = getOrgTree(deptId, deptType, repertoryType, resourceList, token)
    deptIdLists = []
    if deptTitles:                      # 设置资源库文件权限
        for deptTitle in deptTitles:
            deptIdList = [key for key in resp('$..*[@.title is "%s"].key' % deptTitle)]     # [42]
            deptIdLists += deptIdList                                                       # [42] + [78] = [42,78]
        companyRepertoryParamList = RepertoryParamList
        deptRepertoryParamList = []
    else:                               # 设置部门资源文件权限
        companyRepertoryParamList = []
        deptRepertoryParamList = RepertoryParamList

    with pytest.allure.step(
            "文件权限设置 deptIdList={0}，securityLevel={1}，repertoryType={2}，deptRepertoryParamList={3}，companyRepertoryParamList={4}".format(deptIdLists,
                                                                                                             securityLevel,
                                                                                                             repertoryType,
                                                                                                             deptRepertoryParamList,
                                                                                                             companyRepertoryParamList)):
        resp = manageEdmTool.setFilePermissions(deptIdLists, repertoryType, securityLevel, token, deptRepertoryParamList, companyRepertoryParamList)
        assert check_value(resp.message, message)


def visibleTree(flag, token):
    with pytest.allure.step("临时权限设置页面树形结构 flag={0}".format(flag)):
        return manageEdmTool.visibleTree(flag, token)

def visibleCreate(userIdList, repertoryList, token):
    expireTime = gen_expire_time(1)
    reason = gen_random_target()
    with pytest.allure.step(
            "设置资源临时权限 userIdList={0}，repertoryList={1}，expireTime={2}，reason={3}".format(userIdList, repertoryList,
                                                                                         expireTime,
                                                                                         reason)):
        return manageEdmTool.visibleCreate(userIdList, repertoryList, expireTime, reason, token)

def previewContent(repertoryType, resourceId, token, message):
    with pytest.allure.step("文件预览 repertoryType={0}，resourceId={1}，message={2}".format(repertoryType,resourceId,message)):
        resp = manageEdmTool.previewContent(repertoryType, resourceId, token)
        assert check_value(resp.message, message)

def deleteVisibleOrg(deptId, isLastOne, orgId, repertoryType, resourceId, token, message):
    with pytest.allure.step(
            "删除文件可见组织 deptId={0}，isLastOne={1}，repertoryType={2}，orgId={3}，resourceId={4}".format(deptId, isLastOne,
                                                                                                  repertoryType, orgId,
                                                                                                  resourceId)):
        resp = manageEdmTool.deleteVisibleOrg(deptId, isLastOne, orgId, repertoryType, resourceId, token)
        assert check_value(resp.message, message)


@allure.severity("normal")
@allure.feature(u"测试模块_EDM")
@allure.story(u"测试story_部门资源下载文件")
@pytest.mark.parametrize("account,password,repertoryType,depTitle", [
    ('test_edm',  '123456', 1, u'财务部'),
    ('test_edm',  '123456', 1, u'电子组'),
])
def test_deptResourceDownLoadFile(account,password,repertoryType,depTitle):
    """
    部门资源下载文件流程：管理员登录，获得部门资源列表，检索指定目录及其下级目录中的文件，下载选中文件，检验下载文件属性
    """
    token = manageLogin(account,password)('$.data.token')
    # departmentId = getInitDeptResourceMenu(token,depTitle,'value')
    resp = getInitDeptResourceMenu(token, depTitle)
    departmentId = next(resp('$..*[@.title is "%s"].value' % depTitle))
    resp = readFilesByParam(departmentId, True, True, repertoryType,token)
    for fileinfo in resp.data.list:
        if not fileinfo.resourceType:   # 文件类型 --> resourceType=False
            resp = downLoadFile(fileinfo.id, repertoryType, token)
            assert check_value_include(fileinfo.resourceName, resp.data.zipName)
            assert check_value(fileinfo.obsUrl, resp.data.zipUrl)


@allure.severity("normal")
@allure.feature(u"测试模块_EDM")
@allure.story(u"测试story_部门资源输出文件")
@pytest.mark.parametrize("account,password,repertoryType,depTitle,cacheTitle", [
    ('test_edm', '123456', 1, u'财务部', u'内部文档归档输出区'),
    ('test_edm', '123456', 1, u'电子组', u'内部文档归档输出区'),
])
def test_fileOutput(account,password,repertoryType,depTitle,cacheTitle):
    """
    部门资源输出文件流程：管理员登录，获得部门资源列表，检索指定目录及其下级目录中的文件，部门资源下未被输出到缓冲区文件，获得缓冲库资源列表并校验输出文件
    1.部门资源下文件未被输出到缓冲区，则将其输出到缓冲区
    2.部门资源下文件已被输出到缓冲区，则提示文件已经被输出,请重新选择

    """
    token = manageLogin(account, password)('$.data.token')
    resp = getInitDeptResourceMenu(token, depTitle)
    departmentId = next(resp('$..*[@.title is "%s"].value' % depTitle))
    resp = readFilesByParam(departmentId, True, True, repertoryType, token)
    fileOutputIds = [id for id in resp('$..*[@.output is False].id')]               # 部门资源下未被输出到缓冲区文件
    if fileOutputIds:
        resourceNamesDept = [resourceName for resourceName in resp('$..*[@.output is False].resourceName')]
        # resourceIdsDept = [resourceId for resourceId in resp('$..*[@.output is False].id')]
        fileOutput(fileOutputIds, token)
        resp = getInitCacheResourceMenu(token,cacheTitle)
        cacheDirectoryId = next(resp('$..*[@.title is "%s"].key' % cacheTitle))          # 内部文档归档输出区 --> edm_1
        cacheDeptId = next(resp('$..*[@.title is "%s"].value' % cacheTitle))
        resp = readFilesByParam(cacheDeptId, True, False, 2, token, cacheDirectoryId)              #1：部门资源 2：缓存库资源 3：资源库 4：公共资源
        # 查询内外部文档归档输出区文件列表 menuType = False
        # {"fileName":null,"departmentId":1,"pageNo":1,"isMostJunior":true,"menuType":false,"pageSize":20,"repertoryTypeCode":2,"fileNameSort":1,"fileTypeSort":0,"fileSizeSort":0,"createTimeSort":0,"outputTimeSort":0,"directoryId":"edm_1"}
        resourceNamesCashe = [resourceName for resourceName in resp('$..resourceName')]
        # resourceIdsCashe = [resourceId for resourceId in resp('$..id')]
        # assert check_list_include_list(resourceIdsCashe, resourceIdsDept)
        assert check_list_include_list(resourceNamesCashe, resourceNamesDept)
    else:
        fileOutputIds = [id for id in resp('$..*[@.output is True].id')]
        resp = fileOutput(fileOutputIds, token)
        assert check_value_include(resp.message,'已经被输出,请重新选择！')


@allure.severity("normal")
@allure.feature(u"测试模块_EDM")
@allure.story(u"测试story_部门资源收藏文件")
@pytest.mark.parametrize("account,password,repertoryType,depTitle,collectionDept", [
    ('test_edm', '123456',1, u'财务部',u'部门资源'),
    ('test_edm', '123456',1, u'电子组',u'部门资源'),
])
def test_addCollection(account,password,repertoryType,depTitle,collectionDept):
    """
    文件收藏流程：管理员登录，获得部门资源列表，我的收藏资源列表树结构，检索选中目录及其下级目录中的文件，添加收藏，查询收藏列表并校验，取消收藏，查询收藏列表并校验
    """
    token = manageLogin(account, password)('$.data.token')
    resp = getInitDeptResourceMenu(token, depTitle)
    departmentId = next(resp('$..*[@.title is "%s"].value' % depTitle))
    resp = getInitResourceMenu(token,collectionDept)
    directoryId = next(resp('$..*[@.title is "%s"].key' % collectionDept))  # key: "edm_-1"
    resp = readFilesByParam(departmentId, True, True, repertoryType, token)
    for fileinfo in resp.data.list:
        collectionResourceBOS = [{'isFolder': fileinfo.resourceType, 'id': fileinfo.id, 'fileSuffix': fileinfo.fileSuffix,'obsId': fileinfo.obsId, 'resourceName': fileinfo.resourceName}]
        addCollection(collectionResourceBOS, fileinfo.repertoryType, fileinfo.parentId.split('_')[1], token)        # edm_0 --> 0
        resp = readCollectionFilesByParam(directoryId, repertoryType, fileinfo.resourceName.split('.')[0], token)   # nginx.txt查询无结果
        resourceNamesCollection = [resourceName for resourceName in resp('$..resourceName')]
        assert check_list_include_value(resourceNamesCollection,fileinfo.resourceName)
        collectionResourceBOS = [{'id': fileinfo.id, 'fileSuffix': fileinfo.fileSuffix,'obsId': fileinfo.obsId, 'resourceName': fileinfo.resourceName}]
        removeCollection(collectionResourceBOS, fileinfo.repertoryType, token)
        resp = readCollectionFilesByParam(directoryId, repertoryType, fileinfo.resourceName.split('.')[0], token)   # nginx.txt查询无结果
        resourceNamesCollection = [resourceName for resourceName in resp('$..resourceName')]
        assert not check_list_include_value(resourceNamesCollection, fileinfo.resourceName)


@allure.severity("normal")
@allure.feature(u"测试模块_EDM")
@allure.story(u"测试story_部门资源移动文件")
@pytest.mark.parametrize("account,password,depTitle,repertoryType,srcDepFolder,dstDepFolder", [
    ('test_edm', '123456', u'电子组', 1, u'接口测试文件夹1', u'接口测试文件夹2'),
    ('test_edm', '123456', u'电子组', 1, u'接口测试文件夹2', u'接口测试文件夹1'),
])
def test_fileMove(account,password,depTitle,repertoryType,srcDepFolder,dstDepFolder):
    """
    部门资源文件移动流程：管理员登录，获得部门资源列表，获得部门资源下一级权限资源列表(文件夹)，检索选中目录中的文件，移动到部门资源下指定文件夹，校验目的文件夹下是否包含移动文件
    """
    token = manageLogin(account, password)('$.data.token')
    resp = getInitDeptResourceMenu(token, depTitle)
    belongId = next(resp('$..*[@.title is "%s"].key' % depTitle))                   # key: "dept_78"
    orgId = departmentId = next(resp('$..*[@.title is "%s"].value' % depTitle))     # value: "78"
    resp = getNextResourceMenu(repertoryType, token, '', belongId)
    srcDirectoryId = next(resp('$..*[@.title is "%s"].key' % srcDepFolder))         # key: "edm_2737"
    dstDirectoryId = next(resp('$..*[@.title is "%s"].key' % dstDepFolder))         # key: "edm_2736"
    resp = readFilesByParam(departmentId, True, False, repertoryType, token, srcDirectoryId)
    for fileinfo in resp.data.list:
        selectFileMove(orgId, repertoryType, dstDepFolder, fileinfo, token)
        resp = readFilesByParam(departmentId, True, False, repertoryType, token, dstDirectoryId)
        resourceIds = [resourceId for resourceId in resp('$..id')]                  # [u'edm_2586', u'edm_2585', u'edm_2587', u'edm_2588', u'edm_2589', u'edm_2590']
        assert check_list_include_value(resourceIds, fileinfo.id)                   #  u'edm_2586'


@allure.severity("normal")
@allure.feature(u"测试模块_EDM")
@allure.story(u"测试story_创建删除文件")
@pytest.mark.parametrize("account,password,depTitle,repertoryType", [
    ('test_edm', '123456', u'电子组',1),
    ('test_edm', '123456', u'财务部',1),
])
def test_maintainFolder(account,password,depTitle,repertoryType):
    """
    创建删除文件流程：管理员登录，获得部门资源列表，获取指定组织架构下文档菜单，创建随机文档目录，查询并校验新建目录是否存在，删除目录，查询并校验新建目录是否存在
    """
    token = manageLogin(account, password)('$.data.token')
    resp = getInitDeptResourceMenu(token, depTitle)
    belongId = next(resp('$..*[@.title is "%s"].key' % depTitle))           # key: "dept_78"
    departmentId = next(resp('$..*[@.title is "%s"].value' % depTitle))     # value: "78"
    resp = getMaintainInitMenu(repertoryType, 0, token, '', belongId)
    resourceList = [{'id': folder.key, 'resourceName': folder.title} for folder in resp.data]   # 原有目录
    resourceName = gen_random_target()
    resourceList += [{'id': '', 'resourceName': resourceName}]              # 新增目录，id为0或空表示新增
    maintain(departmentId, repertoryType, resourceList, token)
    directoryId = ''                                                        # 查询组织架构无需传directoryId
    resp = readFilesByParam(departmentId, True, True, 1, token, directoryId, resourceName)
    idList = [id for id in resp('$..id')]
    fileRemove(idList, repertoryType, token)
    resp = readFilesByParam(departmentId, True, True, 1, token, directoryId, resourceName)
    assert check_value(resp.data.list, [])

@allure.severity("normal")
@allure.feature(u"测试模块_EDM")
@allure.story(u"测试story_部门资源设置文件权限")
@pytest.mark.parametrize("account,password,depTitle,repertoryType,depFolder,securityLevel", [
    ('test_edm', '123456', u'电子组', 1, u'接口测试文件夹1', 5),  # 四级
    ('test_edm', '123456', u'电子组', 1, u'接口测试文件夹1', 1),  # 特级
])
def test_deptSetFilePermissions(account,password,depTitle,repertoryType,depFolder,securityLevel):
    """
    部门资源设置文件权限流程：管理员登录，获得部门资源列表，获取指定目录下文件列表及文件权限，设置文件权限，获取指定目录下文件列表及文件权限，查询并校验文件权限是否被正确设置
    """
    token = manageLogin(account, password)('$.data.token')
    resp = getInitDeptResourceMenu(token, depTitle)
    deptId = next(resp('$..*[@.title is "%s"].value' % depTitle))               # value: "78"
    resp = readFilesByParam(deptId, True, True, 1, token, '')
    directoryId = next(resp('$..*[@.resourceName is "%s"].id' % depFolder))     # id: "edm_2737"
    resp = readFilesByParam(deptId, True, False, 1, token, directoryId)
    for fileinfo in resp.data.list:
        # resourceList = [{'resourceId': fileinfo.id, 'resourceType': fileinfo.resourceType, 'securityLevel': fileinfo.securityLevel}]
        # getOrgTree(deptId, 2, repertoryType, resourceList, token)
        # deptIdList=[]
        # deptRepertoryParamList = [{'id': fileinfo.id, 'fileSuffix': fileinfo.fileSuffix, 'obsId': fileinfo.obsId,
        #                            'resourceName': fileinfo.resourceName, 'parentIdCode': fileinfo.parentIdCode,
        #                            'resourceType': fileinfo.resourceType}]
        setFilePermissions(deptId, 2, fileinfo, repertoryType, securityLevel, token, None)    #部门组员设置资源权限deptIdList=[]
    resp = readFilesByParam(deptId, True, False, 1, token, directoryId)
    for securityLevel_ in resp('$..securityLevel'):
        assert check_value(securityLevel, securityLevel_)

def setVisible2Preview(repertoryType, resourceId, repertoryIdCode, resourceType, userId, tokenM, tokenE):
    previewContent(repertoryType, resourceId, tokenE, u'无预览权限')
    repertoryList = [{'id': resourceId, 'repertoryIdCode': repertoryIdCode, 'resourceType': resourceType}]
    visibleCreate([userId], repertoryList, tokenM)
    previewContent(repertoryType, resourceId, tokenE, None)


@allure.severity("normal")
@allure.feature(u"测试模块_EDM")
@allure.story(u"测试story_资源库设置资源临时权限")
@pytest.mark.parametrize("account,password,companyName,depFolder,repertoryType,edmAccount,deptName", [
    ('test_edm', '123456', u'晶日', 'api-test', 3, 'edm-huangfg', u'秘书室'),
    ('test_edm', '123456', u'晶日', 'api-test', 3, 'edm-api',     u'电子组'),
])
def test_visibleCreate(account,password,companyName,depFolder,repertoryType,edmAccount,deptName):
    """
    资源库设置文件临时可见流程：管理员登录，获得资源库列表，获取指定目录下文件列表，用户预览提示无权限，获取临时权限设置页面树形结构，设置资源临时权限给用户，用户预览成功
    1.文件有可见组织架构，可见组织架构包含秘书室，说明有权限预览
    2.文件可见组织架构不包含秘书室，用户无权限预览，设置临时权限给用户
    3.文件无可见组织架构，用户无权限预览，设置临时权限给用户
    """
    token = manageLogin(account, password)('$.data.token')
    token_edm = manageLogin(edmAccount, password)('$.data.token')
    resp = getInitCompanyResourceMenu(token)
    departmentId = next(resp('$..*[@.title is "%s"].value' % companyName))      # value: "1" ,key: "dept_1"
    directoryId = next(resp('$..*[@.title is "%s"].value' % depFolder))         # key: "edm_1088"
    resp = visibleTree(1, token)
    userId = next(resp('$..*[@.title is "%s"].value' % edmAccount))             # value: 369
    resp = readFilesByParam(departmentId, True, False, repertoryType, token, directoryId)
    for fileinfo in resp.data.list:
        if not fileinfo.resourceType:                       # 文件类型，文件夹无法预览
            if fileinfo.resourceToDeptInfoBOS:              # 文件有可见组织架构
                if any(deptName == dept.deptName for dept in fileinfo.resourceToDeptInfoBOS) or any(u'晶日' == dept.deptName for dept in fileinfo.resourceToDeptInfoBOS):  # 可见组织架构包含秘书室，说明有权限预览
                    previewContent(repertoryType, fileinfo.id, token_edm, None)
                else:                                                                          # 可见组织架构不包含秘书室，用户无权限预览，设置临时权限给用户
                    setVisible2Preview(repertoryType, fileinfo.id, fileinfo.parentIdCode, fileinfo.resourceType, userId,
                                       token, token_edm)
            else:                                                                               # 无可见组织架构，用户无权限预览，设置临时权限给用户
                setVisible2Preview(repertoryType, fileinfo.id, fileinfo.parentIdCode, fileinfo.resourceType, userId,
                                   token, token_edm)

def selectFileMove(orgId, repertoryType, depFolder, fileinfo, token):
    """
    选择目录并移动文件至指定目录
    """
    resp = selectTreeToFile(orgId, repertoryType,token)                 # {key: 2160, title: "乖乖乖", parentIdCode: "0_2160_", deptType: null, parentId: null, expand: null}
    aimsResourceId = next(resp('$..*[@.title is "%s"].key' % depFolder))
    aimsParentIdCode = next(resp('$..*[@.title is "%s"].parentIdCode' % depFolder))
    resourceInfoList = [
        {'resourceId': fileinfo.id, 'fileSuffix': fileinfo.fileSuffix, 'obsId': fileinfo.obsId,
         'resourceName': fileinfo.resourceName, 'parentIdCode': fileinfo.parentIdCode,
         'parentId': fileinfo.parentId, 'orgId': fileinfo.departmentId,
         'fileType': 1 if fileinfo.resourceType else 0}]                # resourceType True 表示文件夹 --> 文件 0 | 文件夹 1
    resp = fileMove(orgId, aimsParentIdCode, aimsResourceId, 1, resourceInfoList, token)
    assert check_value(resp.data, u'移动文件成功')

@allure.severity("normal")
@allure.feature(u"测试模块_EDM")
@allure.story(u"测试story_资源库设置资源临时权限-移动文件")
@pytest.mark.parametrize("account,password,companyName,depFolder,repertoryType,edmAccount,deptName", [
    ('test_edm', '123456', u'晶日',u'接口测试-勿动', 3, 'edm-huangfg', u'秘书室'),
    ('test_edm', '123456', u'晶日',u'接口测试-勿动', 3, 'edm-api',     u'电子组'),
])
def test_visibleCreateAndMove(account,password,companyName,depFolder,repertoryType,edmAccount,deptName):
    """
    资源库移动文件流程：临时可见权限无法移动文件，管理员登录，获得资源库列表，获取指定目录下文件列表，用户预览提示无权限，获取临时权限设置页面树形结构，设置资源临时权限给用户，用户预览成功，无权限移动文件
    1.文件有可见组织架构，可见组织架构包含秘书室，说明有权限预览
    2.文件可见组织架构不包含秘书室，用户无权限预览，设置临时权限给用户，无权限移动文件
    3.文件无可见组织架构，用户无权限预览，设置临时权限给用户，无权限移动文件
    """
    token = manageLogin(account, password)('$.data.token')
    token_edm = manageLogin(edmAccount, password)('$.data.token')
    resp = getInitCompanyResourceMenu(token)
    orgId = departmentId = next(resp('$..*[@.title is "%s"].value' % companyName))  # value: "1",    key: "dept_1",   menuType: true  --> 组织
    directoryId = next(resp('$..*[@.title is "%s"].value' % depFolder))             # value: "1088", key: "edm_1088", menuType: false --> 自定义目录
    resp = visibleTree(1, token)
    userId = next(resp('$..*[@.title is "%s"].value' % edmAccount))  # value: 369
    resp = readFilesByParam(departmentId, True, False, repertoryType, token, directoryId)
    for fileinfo in resp.data.list:
        if not fileinfo.resourceType:                       # 文件类型，文件夹无法预览
            if fileinfo.resourceToDeptInfoBOS:              # 文件有可见组织架构
                if any(deptName == dept.deptName for dept in fileinfo.resourceToDeptInfoBOS) or any(u'晶日' == dept.deptName for dept in fileinfo.resourceToDeptInfoBOS):  # 可见组织架构包含秘书室，说明有权限预览
                    previewContent(repertoryType, fileinfo.id, token_edm, None)
                    selectTreeToOrg(orgId, repertoryType, fileinfo, token_edm, None)
                    selectFileMove(orgId, repertoryType, depFolder, fileinfo, token_edm)
                else:                                                                          # 可见组织架构不包含秘书室，用户无权限预览，设置临时权限给用户
                    setVisible2Preview(repertoryType, fileinfo.id, fileinfo.parentIdCode, fileinfo.resourceType, userId,
                                       token, token_edm)
                    selectTreeToOrg(orgId, repertoryType, fileinfo, token_edm, u'您权限不足，无法移动！')
            else:                                                                               # 无可见组织架构，用户无权限预览，设置临时权限给用户
                setVisible2Preview(repertoryType, fileinfo.id, fileinfo.parentIdCode, fileinfo.resourceType, userId,
                                   token, token_edm)
                selectTreeToOrg(orgId, repertoryType, fileinfo, token_edm, u'您权限不足，无法移动！')


@allure.severity("normal")
@allure.feature(u"测试模块_EDM")
@allure.story(u"测试story_资源库下载文件")
@pytest.mark.parametrize("account,password,companyName,depFolder,repertoryType,edmAccount,deptName", [
    ('test_edm', '123456', u'晶日', 'api-test', 3, 'edm-huangfg', u'秘书室'),
    ('test_edm', '123456', u'晶日', 'api-test', 3, 'edm-api',     u'电子组'),
])
def test_companyResourceDownLoadFile(account,password,companyName,depFolder,repertoryType,edmAccount,deptName):
    """
    资源库下载文件流程：管理员登录，获得部门资源列表，检索指定目录及其下级目录中的文件，下载选中文件，检验下载文件属性
    1.资源库特级、一级、二级文件不允许下载1,2,3
    2.用户在可见组织架构内
    3.用户等级高于资源文件等级
    """
    token = manageLogin(account, password)('$.data.token')
    token_edm = manageLogin(edmAccount, password)('$.data.token')
    resp = getInitCompanyResourceMenu(token)
    departmentId = next(resp('$..*[@.title is "%s"].value' % companyName))  # value: "1",    key: "dept_1",   menuType: true  --> 组织
    directoryId = next(resp('$..*[@.title is "%s"].value' % depFolder))             # value: "1088", key: "edm_1088", menuType: false --> 自定义目录
    # resp = visibleTree(1, token)
    # userId = next(resp('$..*[@.title is "%s"].value' % edmAccount))  # value: 369
    resp = readFilesByParam(departmentId, True, False, repertoryType, token, directoryId)
    for fileinfo in resp.data.list:
        if not fileinfo.resourceType:                       # 文件类型 --> resourceType=False
            if fileinfo.resourceToDeptInfoBOS:              # 文件有可见组织架构
                if any(deptName == dept.deptName for dept in fileinfo.resourceToDeptInfoBOS) or any(u'晶日' == dept.deptName for dept in fileinfo.resourceToDeptInfoBOS):  # 可见组织架构包含秘书室或者晶日代表对所有人可见
                    if fileinfo.securityLevel >= 4:         # 三级、四级文件，用户资源库权限为特级1
                        resp = downLoadFile(fileinfo.id, repertoryType, token_edm)
                        assert check_value_include(fileinfo.resourceName, resp.data.zipName)
                        assert check_value(fileinfo.obsUrl, resp.data.zipUrl)
                    else:
                        resp = downLoadFile(fileinfo.id, repertoryType, token_edm)
                        assert check_value(resp.message, u'人员权限不足，请联系文控中心人员进行下载！')
                else:
                    resp = downLoadFile(fileinfo.id, repertoryType, token_edm)
                    assert check_value(resp.message, u'人员权限不足，请联系文控中心人员进行下载！')

@allure.severity("normal")
@allure.feature(u"测试模块_EDM")
@allure.story(u"测试story_资源库设置文件权限")
@pytest.mark.parametrize("account,password,companyName,depFolder,repertoryType,edmAccount,deptName,visibleDeptNames", [
    ('test_edm', '123456', u'晶日', 'api-test', 3, 'edm-huangfg', u'秘书室', [u'秘书室', u'人资部']),
    ('test_edm', '123456', u'晶日', 'api-test', 3, 'edm-api',     u'电子组', [u'秘书室', u'电子组']),
])
def test_companySetFilePermissions(account,password,companyName,depFolder,repertoryType,edmAccount,deptName,visibleDeptNames):
    """
    资源库设置文件权限流程：管理员登录，获得部门资源列表，检索指定目录及其下级目录中的文件，选中文件设置权限，检验设置权限
    1.文件可见组织架构是晶日允许用户设置文件权限
    2.用户在可见组织架构内允许设置文件权限
    3.用户不在可见组织架构内不允许设置文件权限
    """
    token = manageLogin(account, password)('$.data.token')
    token_edm = manageLogin(edmAccount, password)('$.data.token')
    resp = getInitCompanyResourceMenu(token)
    deptId = departmentId = next(resp('$..*[@.title is "%s"].value' % companyName))          # value: "1",    key: "dept_1",   menuType: true  --> 组织
    directoryId = next(resp('$..*[@.title is "%s"].value' % depFolder))                      # value: "1088", key: "edm_1088", menuType: false --> 自定义目录
    resp = readFilesByParam(departmentId, True, False, repertoryType, token, directoryId)
    for fileinfo in resp.data.list:
        if not fileinfo.resourceType:                       # 文件类型 --> resourceType=False
            if fileinfo.resourceToDeptInfoBOS:              # 文件有可见组织架构
                if any(deptName == dept.deptName for dept in fileinfo.resourceToDeptInfoBOS) or any(
                        u'晶日' == dept.deptName for dept in fileinfo.resourceToDeptInfoBOS): # 可见组织架构包含秘书室或者晶日代表对所有人可见
                    # if deptName in visibleDeptNames:
                    setFilePermissions(deptId, 1, fileinfo, repertoryType, 3, token_edm, None, visibleDeptNames)
                    setFilePermissions(deptId, 1, fileinfo, repertoryType, fileinfo.securityLevel, token_edm, None, visibleDeptNames)   # 资源库deptType=1
                    # else:
                    #     setFilePermissions(deptId, 1, fileinfo, repertoryType, 3, token_edm,u'您权限不足，无法设置！', visibleDeptNames)    # 资源库deptType=1
                else:
                    setFilePermissions(deptId, 1, fileinfo, repertoryType, 3, token_edm, u'您权限不足，无法设置！', visibleDeptNames)       # 资源库deptType=1


@allure.severity("normal")
@allure.feature(u"测试模块_EDM")
@allure.story(u"测试story_资源库删除文件可见组织")
@pytest.mark.parametrize("account,password,companyName,depFolder,repertoryType,edmAccount,deptName,visibleDeptNames", [
    ('test_edm', '123456', u'晶日', 'api-test', 3, 'edm-huangfg', u'秘书室', [u'秘书室', u'人资部']),
    # ('test_edm', '123456', u'晶日', 'api-test', 3, 'edm-api',     u'电子组', [u'法务组', u'电子组']),
])
def test_companyDeleteVisibleOrg(account,password,companyName,depFolder,repertoryType,edmAccount,deptName,visibleDeptNames):
    """
    资源库删除文件可见组织流程：管理员登录，获得部门资源列表，检索指定目录及其下级目录中的文件，选中文件设置权限，检验设置权限
    1.文件可见组织架构是晶日允许用户删除文件可见组织
    2.用户在可见组织架构内允许删除文件可见组织
    3.用户不在可见组织架构内不允许删除文件可见组织
    """
    token = manageLogin(account, password)('$.data.token')
    token_edm = manageLogin(edmAccount, password)('$.data.token')
    resp = getInitCompanyResourceMenu(token)
    deptId = departmentId = next(resp('$..*[@.title is "%s"].value' % companyName))          # value: "1",    key: "dept_1",   menuType: true  --> 组织
    directoryId = next(resp('$..*[@.title is "%s"].value' % depFolder))                      # value: "1088", key: "edm_1088", menuType: false --> 自定义目录
    resp = readFilesByParam(departmentId, True, False, repertoryType, token, directoryId)
    for fileinfo in resp.data.list:
        if not fileinfo.resourceType:                       # 文件类型 --> resourceType=False
            if fileinfo.resourceToDeptInfoBOS:              # 文件有可见组织架构
                if any(deptName == dept.deptName for dept in fileinfo.resourceToDeptInfoBOS) or any(
                        u'晶日' == dept.deptName for dept in fileinfo.resourceToDeptInfoBOS): # 可见组织架构包含秘书室或者晶日代表对所有人可见
                    for orginfo in fileinfo.resourceToDeptInfoBOS:
                        if orginfo.deptName != deptName:
                            deleteVisibleOrg(deptId, False, orginfo.deptId, repertoryType, fileinfo.id, token_edm, None)    # 删除可见组织
                else:
                    for orginfo in fileinfo.resourceToDeptInfoBOS:
                        deleteVisibleOrg(deptId, False, orginfo.deptId, repertoryType, fileinfo.id, token_edm, u'您权限不足，无法删除')