#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on June 12, 2019
@author: hzhuangfg
'''
import json
import time
import traceback
from fs.Trace import Trace
from check.checkDB import CheckDB
from engine.db import MySQLet,Const
from com.json_processor import JSONProcessor
from com.api import logging
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式

class CheckResult():
    def __init__(self,logId,env='test',http_client=None):
        self.env = env
        self.logId = logId
        self.checkdb = CheckDB(self.logId,self.env)
        self.http_client = http_client            #locust client or requests cient


    def __dealwithPrivateResp__(self,resp):
        """
        :param resp:
        :return:
        """
        Logger = Trace("CheckHoolinkBase::__dealwithPrivateResp__")
        try:
            if resp is not None and  resp.has_key('data'):
                if resp.result == 'success' or resp.biz_code == 'GPBIZ_00':     #resp.biz_msg == u'接口调用成功，订单已授理',msg="订单授予成功",msg="提交成功",
                    return resp.data if isinstance(resp.data,dict) else JSONProcessor(json.loads(resp.data,encoding='utf-8'))
            return None
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return None

    def __dealwithGatewayResp__(self,resp):
        """
        :param resp:
        :return:
        """
        Logger = Trace("CheckHoolinkBase::__dealwithGatewayResp__")
        try:
            if resp:
                # Logger.info(self.logId,'body = %s'%(json.dumps(resp,ensure_ascii=False,indent=4).decode('utf8')))
                if resp.status == True and resp.msgMode == 'PROMPT':
                    if resp is not None and resp.has_key('data'):
                            return resp.data if isinstance(resp.data,dict) else JSONProcessor(json.loads(resp.data,encoding='utf-8'))
            return None
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return None


    def __dealwithDeviceResp__(self,resp):
        """
        :param resp:
        :return:
        """
        Logger = Trace("CheckHoolinkBase::__dealwithDeviceResp__")
        try:
            if resp is not None:
                if resp.status is True and resp.has_key('data'):
                    return True
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def __deleteByField(self,db,table,fieldkey,fieldvalue):
        """
        """
        Logger = Trace("CheckResult::__deleteByField")
        try:
            sql = 'delete from %s where %s = %s'%(table,fieldkey,fieldvalue)
            return self.checkdb.updateByField(sql,db)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return None


    def __existByRecord(self,db,table,**params):
        """
        记录存在返回True，不存在返回False
        """
        Logger = Trace("CheckResult::__existByRecord")
        try:
            return self.checkdb.existByRecord(db,table,**params)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return None

    def __deleteByRecord(self,db,table,**params):
        """
        """
        Logger = Trace("CheckResult::__deleteByRecord")
        try:
            return self.checkdb.deleteByRecord(db,table,**params)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return None


    def __updateByRecord(self,db,table,**params):
        """
        """
        Logger = Trace("CheckResult::__updateByRecord")
        try:
            return self.checkdb.updateByRecord(db,table,**params)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return None

    def __checkByRecord(self,db,table,**kwargs):
        """
        """
        Logger = Trace("CheckResult::__checkByRecord")
        try:
            # sql = 'select * from %s where %s = %s'%(table,fieldkey,fieldvalue)
            # return self.checkdb.checkField(db, table, **kwargs)
            Logger.info(kwargs)
            return self.checkdb.checkRecord(db,table,**kwargs)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return None

    def __checkByField(self,schma,table,fieldkey,fieldvalue,**kwargs):
        """
        """
        Logger = Trace("CheckResult::__checkByField")
        try:
            sql = 'select * from %s where %s = %s'%(table,fieldkey,fieldvalue)
            return self.checkdb.checkField(sql,schma,**kwargs)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return None

    def __checkFieldByFilter(self,db_name,table_name,**criteria):
        """
        """
        Logger = Trace("CheckResult::__checkBillFieldByFilter")
        try:
            mysqlet = MySQLet(host=Config.dbhost, user= Config.dbuser, password=Config.dbpass, charset="utf8", database=db_name, port=Config.dbport)
            record = JSONProcessor(mysqlet.findKeySql(Const.FIND_BY_ATTR, table=table_name, criteria=criteria))
            Logger.debug('record = %s'%record)
            # mysqlet.findKeySql(Const.FIND_BY_ATTR, table="Bill", criteria= {"where": "businessRecordNumber=1418021214354520002"})
            # sql = 'select * from Bill where ' + Filter
            # return self.checkdb.checkFieldByFilter(record,**kwargs)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return None




    def __waitRemainPay(self,businessrecordnumber,**kwargs):
        """
        """
        Logger = Trace("CheckResult::__waitRemainPayStatus")
        try:
            i = 1
            while not self.__checkRemainPayByOrderNumber(businessrecordnumber,**kwargs):
                time.sleep(1)
                i += 1
                if i >= 10: #等待10s
                    return False
            else:
                return True
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False


    def check_debitQuickPayAndBalancePay(self,preOrder_brn,refund_brn,debitPay_brn):
        """
        bill表：消费单成功，充值单已撤销，充撤单成功
        渠道表：充值单已撤，充退单成功
        remainpay转账成功：消费网关过渡户 - 退款网关过渡户
        """
        Logger = Trace("CheckResult::check_debitQuickPayAndBalancePay")
        try:
            if self.check_billStatusByBrn(preOrder_brn,status=u'成功',transactionType=u'消费'):
                if self.check_billStatusByBrn(debitPay_brn,status=u'已撤销',transactionType=u'充值',fromAccountNumber='990305001001'):
                    if self.check_billStatusByBrn(refund_brn,status=u'成功',transactionType=u'充撤',fromAccountNumber='990305001001',toAccountNumber='990305001003'):
                        if self.check_remainPayStatusByBrn(refund_brn,status=u'成功',transactionType=u'转账',fromAccountNumber='990305001001',toAccountNumber='990305001003'):
                            if self.check_AccountRechargeOrderByBrn(debitPay_brn,status=u'已撤',transactionType=u'充值',accountNumber='990305001001'):
                                return self.check_AccountRechargeOrderByBrn(refund_brn,status=u'成功',transactionType=u'充退',accountNumber='990305001003')
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return None

    def check_playScreenConfig(self,resp,screen_status):
        """
        """
        Logger = Trace("CheckResult::check_playRealTimeMusic")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink-test',table='device_screen',criteria={"select":"*","where":"screen_id=%s"%resp.data.deviceCmdResultMap.keys()[0]},
                                            screen_status=screen_status)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False


    def check_playRealTimeMusic(self,resp,broadcast_config_id,broadcast_config_name,play_mode,play_status):
        """
        """
        Logger = Trace("CheckResult::check_playRealTimeMusic")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink-test',table='broadcast_play_config',criteria={"select":"*","where":"broadcast_config_id=%s"%broadcast_config_id},
                                            broadcast_config_name=broadcast_config_name,play_mode=play_mode,play_status=play_status)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    @logging("CheckResult", "check_createUser")
    def check_createUser(self,resp,account, roleId, name, sex):
        """
        """
        if self.__dealwithDeviceResp__(resp):
            return self.__checkByRecord(db='hoolink_base',table='base_user',criteria={"select":"*","where":"id=%s"%resp.data},
                                        reset_password=1,enabled=1,role_id=roleId,user_account=account,user_name=name,sex=sex)
        return False

    @logging("CheckResult", "check_removeUser")
    def check_removeUser(self,resp,userId,enabled):
        """
        """
        if self.__dealwithDeviceResp__(resp):
            enabled = 1 if enabled is True else 0
            return self.__checkByRecord(db='hoolink_base',table='base_user',criteria={"select":"enabled","where":"id=%s"%userId},
                                        enabled=enabled)
        return False

    @logging("CheckResult", "check_updateStatus")
    def check_updateStatus(self,resp,userId,user_status):
        """
        """
        if self.__dealwithDeviceResp__(resp):
            return self.__checkByRecord(db='hoolink_base',table='base_user',criteria={"select":"user_status","where":"id=%s"%userId},
                                        user_status=user_status)
        return False

    def check_updateUserSex(self,resp,userId,sex):
        """
        """
        Logger = Trace("CheckResult::check_updateUserSex")
        try:
            if self.__dealwithDeviceResp__(resp):
                sex = '1' if sex is True else '0'
                return self.__checkByRecord(db='hoolink_base',table='base_user',criteria={"select":"sex","where":"id=%s"%userId},
                                            sex=sex)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_updateUserName(self,resp,userId,name):
        """
        """
        Logger = Trace("CheckResult::check_updateUserName")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_base',table='base_user',criteria={"select":"user_name","where":"id=%s"%userId},
                                            user_name=name)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_createArea(self,resp):
        """
        """
        Logger = Trace("CheckResult::check_createArea")
        try:
            if self.__dealwithDeviceResp__(resp):
                enabled = 1 if resp.data.baseAreaWithBLOBs.enabled is True else 0
                return self.__checkByRecord(db='hoolink_base', table='base_area',
                                            criteria={"select": "area_desc,area_name,project_id,enabled",
                                                      "where": "area_id=%s" % resp.data.baseAreaWithBLOBs.areaId},
                                            area_desc=resp.data.baseAreaWithBLOBs.areaDesc,
                                            area_name=resp.data.baseAreaWithBLOBs.areaName,
                                            project_id=resp.data.baseAreaWithBLOBs.projectId,
                                            enabled=enabled)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_updateArea(self,resp):
        """
        """
        Logger = Trace("CheckResult::check_updateArea")
        try:
            if self.__dealwithDeviceResp__(resp):
                if resp.data.areaDesc and resp.data.areaName:
                    return self.__checkByRecord(db='hoolink_base',table='base_area',criteria={"select":"area_name,area_desc","where":"area_id=%s"%resp.data.areaId},
                                            area_name=resp.data.areaName,area_desc=resp.data.areaDesc)
                elif resp.data.areaDesc:
                    return self.__checkByRecord(db='hoolink_base',table='base_area',criteria={"select":"area_desc","where":"area_id=%s"%resp.data.areaId},
                                                area_desc=resp.data.areaDesc)
                elif resp.data.areaName:
                    return self.__checkByRecord(db='hoolink_base',table='base_area',criteria={"select":"area_name","where":"area_id=%s"%resp.data.areaId},
                                                area_name=resp.data.areaName)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_deleteArea(self,resp,areaId):
        """
        """
        Logger = Trace("CheckResult::check_deleteArea")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_base',table='base_area',criteria={"select":"enabled","where":"area_id=%s"%areaId},
                                            enabled=0)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False


    def check_updatePoleMutualConversion(self,resp,areaId,poleId):
        """
        """
        Logger = Trace("CheckResult::check_updatePoleMutualConversion")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_device',table='device_pole',criteria={"select":"area_id","where":"pole_id=%s"%poleId},
                                            area_id=areaId)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_createRoad(self,resp, poleIdList):
        """
        """
        Logger = Trace("CheckResult::check_createRoad")
        try:
            if self.__dealwithDeviceResp__(resp):
                for poleId in poleIdList:
                    if not self.__checkByRecord(db='hoolink_device', table='device_pole',
                                                criteria={"select": "road_id", "where": "pole_id=%s" % poleId},
                                                road_id=resp.data):
                        return False
                return True
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_updateRoad(self,resp):
        """
        """
        Logger = Trace("CheckResult::check_updateRoad")
        try:
            if self.__dealwithDeviceResp__(resp):
                record = self.checkdb.printRecord(db='hoolink_base', table='base_road', criteria={"select": "*","where": "id=%s" % resp('$.data.id')})
                return self.compare_resp_record(resp('$.data'),record,exclude_field='id')
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False


    def check_deleteRoad(self,resp, roadId):
        """
        """
        Logger = Trace("CheckResult::check_deleteRoad")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_base', table='base_road',
                                            criteria={"select": "enabled", "where": "id=%s" % roadId},
                                            enabled=0)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_createProject(self,resp,sceneId,projectAddress,projectContacts,projectDesc,projectLat,projectLon,projectName,projectPhone,projectLogoId,projectViewId):
        """
        """
        Logger = Trace("CheckResult::check_createProject")
        try:
            if self.__dealwithDeviceResp__(resp):
                # return self.__checkByRecord(db='hoolink-test',table='device_scene_manage',criteria={"select":"scene_id,project_address,project_contacts,project_desc,project_lat,project_lon,project_name,project_phone,project_logo_id,project_view_id","where":"project_id=%s"%resp.data},
                #                             scene_id=sceneId,project_address=projectAddress,project_contacts=projectContacts,project_desc=projectDesc,project_lat=projectLat,project_lon=projectLon,project_name=projectName,project_phone=projectPhone,project_logo_id=projectLogoId,project_view_id=projectViewId)
                return self.__checkByRecord(db='hoolink_base', table='base_project', criteria={
                    "select": "scene_id,project_address,project_contacts,project_desc,project_lat,project_lon,project_name,project_phone,project_logo_id,project_view_id",
                    "where": "project_id=%s" % resp.data.baseProject.projectId},
                                            scene_id=sceneId, project_address=projectAddress,
                                            project_contacts=projectContacts, project_desc=projectDesc,
                                            project_lat=projectLat, project_lon=projectLon, project_name=projectName,
                                            project_phone=projectPhone, project_logo_id=projectLogoId,
                                            project_view_id=projectViewId)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False


    def compare_resp_record(self,resp,record,exclude_field=''):
        """
        projectId,project_id --> projectid
         {u'project_view_id': 1550, u'project_logo_id': 1549, u'scene_id': 1,}
         {"projectId":226,"projectLogoId":null,""sceneId":1,}
        :param resp:
        :param record:
        :param exclude_field:
        :return:
        """
        Logger = Trace("CheckResult::compare_resp_record")
        try:
            for k,v in resp.iteritems():
                if v:
                    if k.lower() == 'enabled':
                        v = 1 if v == True else 0
                    for rk,rv in record.iteritems():
                        tmpk = ''.join(rk.split('_')).lower()       # project_logo_id --> projectlogoid
                        if k.lower() == tmpk.lower():
                            # Logger.debug('k=%s,v=%s,rk=%s,rv=%s' % (k, v, rk, rv))
                            if str(k.lower()) != exclude_field:
                                if str(v).find(str(rv)) == -1 and str(rv).find(str(v)) == -1:   #rk=road_lat,v=25.34685,rv=25.346850000000
                                    Logger.error('k=%s,v=%s,rk=%s,rv=%s'%(k,v,rk,rv))
                                    return False
            return True
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId, "error: %s" % errMsg)
            return False

    def check_updateProject(self,resp):
        """
        """
        Logger = Trace("CheckResult::check_updateProject")
        try:
            if self.__dealwithDeviceResp__(resp):
                baseProject = resp.data.baseProject
                record = self.checkdb.printRecord(db='hoolink_base', table='base_project', criteria={"select": "*","where": "project_id=%s" % baseProject.projectId})
                return self.compare_resp_record(resp('$.data.baseProject'),record,exclude_field='updated')
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_operationProjectDeviceConfig(self,resp,projectId,deviceTypeIds):
        """
        {
            records:[
                        {'device_sub_type_id': 1L}, {'device_sub_type_id': 2L}, {'device_sub_type_id': 3L}, {'device_sub_type_id': 4L},
                        {'device_sub_type_id': 5L}, {'device_sub_type_id': 6L}, {'device_sub_type_id': 7L}, {'device_sub_type_id': 8L},
                        {'device_sub_type_id': 9L}
                    ]
        }
        "deviceTypeIds": [1, 2, 3, 4, 5, 6, 7, 8, 9]}
        """
        Logger = Trace("CheckResult::check_operationProjectDeviceConfig")
        try:
            if self.__dealwithDeviceResp__(resp):
                sql = "select device_sub_type_id from middle_project_device where project_id = %s"%projectId
                records = self.checkdb.getFields(sql,'hoolink_device')
                Logger.debug('records = %s'%records)
                records = JSONProcessor({'records':records})
                for deviceTypeId in deviceTypeIds:
                    if not deviceTypeId in records('$..*[@.device_sub_type_id is %s].device_sub_type_id'%deviceTypeId):
                        return False
                return True
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False


    def check_deleteProjectDeviceConfig(self,resp,projectId,deviceTypeIds):
        """
        {
            records:[
                        {'device_sub_type_id': 2L}, {'device_sub_type_id': 3L}, {'device_sub_type_id': 4L},{'device_sub_type_id': 5L},
                        {'device_sub_type_id': 6L}, {'device_sub_type_id': 7L}, {'device_sub_type_id': 8L},{'device_sub_type_id': 9L}
                    ]
        }
        "deviceTypeIds": [1]}
        """
        Logger = Trace("CheckResult::check_deleteProjectDeviceConfig")
        try:
            if self.__dealwithDeviceResp__(resp):
                sql = "select device_sub_type_id from middle_project_device where project_id = %s"%projectId
                records = self.checkdb.getFields(sql,'hoolink_device')
                Logger.debug('records = %s'%records)
                records = JSONProcessor({'records':records})
                for deviceTypeId in deviceTypeIds:
                    if deviceTypeId in records('$..*[@.device_sub_type_id is %s].device_sub_type_id'%deviceTypeId):
                        return False
                return True
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_createProjectAreaConfig(self,resp,projectId,projectAreaName,projectAreaDesc):
        """
        {
            records:[
                        {'project_area_name': u'25782595901', 'project_area_desc': u'79304007555'}
                    ]
        }
        "projectAreaName": 25782595901
        "projectAreaDesc": 79304007555
        """
        Logger = Trace("CheckResult::check_createProjectAreaConfig")
        try:
            if self.__dealwithDeviceResp__(resp):
                sql = "select project_area_name,project_area_desc from project_area where project_id = %s"%projectId
                records = self.checkdb.getFields(sql,'hoolink_factory')
                Logger.debug('records = %s'%records)    #[{'project_area_name': u'02680302032', 'project_area_desc': u'15407353844'}]
                records = JSONProcessor({'records':records})
                if (projectAreaName in records('$..*[@.project_area_name is %s].project_area_name'%projectAreaName) and projectAreaDesc in records('$..*[@.project_area_desc is %s].project_area_desc'%projectAreaDesc)):
                    return True
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_createRoleDetail(self,resp):
        """
        """
        Logger = Trace("CheckResult::check_createRoleDetail")
        try:
            if self.__dealwithDeviceResp__(resp):
                enabled = 1 if resp.data.enabled is True else 0
                return self.__checkByRecord(db='hoolink_base', table='base_role', criteria={
                    "select": "enabled,creator,role_name,role_parent,role_parent_code,role_desc,create_user",
                    "where": "role_id=%s" % resp.data.roleId},
                                            enabled=enabled,creator=resp.data.creator, role_name=resp.data.roleName,
                                            role_parent=resp.data.roleParent,role_parent_code=resp.data.roleParentCode,
                                            role_desc=resp.data.roleDesc,create_user=resp.data.createUser)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_updateRole(self,resp):
        """
        """
        Logger = Trace("CheckResult::check_updateRole")
        try:
            if self.__dealwithDeviceResp__(resp):
                record = self.checkdb.printRecord(db='hoolink_base', table='base_role', criteria={"select": "*","where": "role_id=%s" % resp.data.roleId})
                return self.compare_resp_record(resp('$.data'),record,exclude_field='updated')
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_readDeviceList(self,resp):
        """
        接口返回poleDesc 与 db pole_desc字段不一致
        """
        Logger = Trace("CheckResult::check_readDeviceList")
        try:
            if self.__dealwithDeviceResp__(resp):
                for data in resp.data:
                    enabled = 1 if data.enabled == True else 0
                    if not self.__checkByRecord(db='hoolink-test', table='device_pole',
                                            criteria={"select": "*",
                                                      "where": "pole_id=%s" % data.poleId},area_id=data.areaId,pole_address=data.poleAddress, project_id=data.projectId,creator=data.creator,
                                                x_axis=data.xAxis,y_axis=data.yAxis,z_axis=data.zAxis,enabled=enabled,pole_name=data.poleName,pole_no=data.poleNo,pole_status=data.poleStatus,
                                                pole_type_id=data.poleTypeId,pole_desc=data.poleDesc):
                        return False
                return True
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_createSceneManage(self,resp,projectId,manageName,manageDesc):
        """
        """
        Logger = Trace("CheckResult::check_createSceneManage")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_device',table='device_scene_manage',criteria={"select":"project_id,manage_name,manage_desc","where":"id=%s"%resp.data},
                                            project_id=projectId,manage_name=manageName,manage_desc=manageDesc)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False


    def check_updateSceneManage(self,resp,manageName,manageDesc):
        """
        """
        Logger = Trace("CheckResult::check_updateSceneManage")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_device',table='device_scene_manage',criteria={"select":"manage_name,manage_desc","where":"id=%s"%resp.data},manage_name=manageName,manage_desc=manageDesc)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_deleteSceneManage(self,resp):
        """
        """
        Logger = Trace("CheckResult::check_deleteSceneManage")
        try:
            if self.__dealwithDeviceResp__(resp):
                return not self.__existByRecord(db='hoolink_device',table='device_scene_manage',params={"id":resp.data})
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_selectSceneManage(self,resp):
        """
        """
        Logger = Trace("CheckResult::check_selectSceneManage")
        try:
            if self.__dealwithDeviceResp__(resp):
                status = 1 if resp.data.status==True else 0
                return self.__checkByRecord(db='hoolink-test', table='device_scene_manage',
                                            criteria={"select": "creator,project_id,status,manage_name,manage_desc,manage_img",
                                                      "where": "id=%s" % resp.data.id},creator=resp.data.creator,status=status, project_id=resp.data.projectId,manage_name=resp.data.manageName,
                                            manage_desc=resp.data.manageDesc,manage_img=resp.data.manageImg)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_onOffSceneManage(self,resp,manageId,status):
        """
        """
        Logger = Trace("CheckResult::check_onOffSceneManage")
        try:
            status = 1 if status is True else 0
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_device',table='device_scene_manage',criteria={"select":"status","where":"id=%s"%manageId},status=status)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False


    def check_readStrategyConflict(self,resp,status):
        """
        """
        Logger = Trace("CheckResult::check_readStrategyConflict")
        try:
            status = 1 if status is True else 0
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_device',table='device_scene_manage',criteria={"select":"status","where":"id=%s"%resp.data},status=status)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_createLightingScene(self,resp,manageId,onTimeStr,offTimeStr,timeType,lightIds,dimmingValue,dayTime,weekTime):
        """
        device_type = 5 表示单灯
        """
        Logger = Trace("CheckResult::createLightingScene")
        try:
            if self.__dealwithDeviceResp__(resp):
                sql = "select t.* ,t1.*  from device_time_strategy t1,middle_pole_manage t where t1.manage_id = '%s' and t1.device_type = 5 and t1.strategy_id = t.strategy_id" % manageId
                if isinstance(weekTime,list) and weekTime:
                    weekTime = ",".join('%s'%t for t in weekTime)   #列表转字符串：[2,3,4] --> '2,3,4'
                return self.checkdb.checkFields(sql, 'hoolink_device',on_time=onTimeStr,off_time=offTimeStr,time_type=timeType,device_id=lightIds,dimming_value=dimmingValue,day_time=dayTime,week_time=weekTime)
                # return self.__checkByRecord(db='hoolink-test',table='device_scene_manage',criteria={"select":"status","where":"id=%s"%resp.data},status=status)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_createScreenScene(self,resp,manageId,onTimeStr,offTimeStr,timeType,dimmingValue,dayTime,weekTime):
        """
        device_type = 1 表示显示屏
        """
        Logger = Trace("CheckResult::check_createScreenScene")
        try:
            if self.__dealwithDeviceResp__(resp):
                sql = "select t.* ,t1.*  from device_time_strategy t1,middle_strategy_config t where t1.manage_id = '%s' and t1.device_type = 1 and t1.strategy_id = t.strategy_id" % manageId
                if isinstance(weekTime,list) and weekTime:
                    weekTime = ",".join('%s'%t for t in weekTime)   #列表转字符串：[2,3,4] --> '2,3,4'
                return self.checkdb.checkFields(sql, 'hoolink_device',on_time=onTimeStr,off_time=offTimeStr,time_type=timeType,dimming_value=dimmingValue,day_time=dayTime,week_time=weekTime)
                # return self.__checkByRecord(db='hoolink-test',table='device_scene_manage',criteria={"select":"status","where":"id=%s"%resp.data},status=status)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_createPole(self,resp, projectId, areaId, lights, poleName, poleNo, poleDesc,poleAddress):
        """
        """
        Logger = Trace("CheckResult::check_createPole")
        try:
            if self.__dealwithDeviceResp__(resp):
                if lights:
                    # lights = lights[0]
                    sql = "select t1.* ,t.*  from device_light t,device_pole t1 where t1.pole_id = '%s' and t1.pole_id = t.pole_id" % resp.data
                    return self.checkdb.checkFields(sql, 'hoolink_device',project_id=projectId,area_id=areaId,light_mac_address=lights('$.lightMacAddress'),pole_name=poleName,pole_no=poleNo,pole_desc=poleDesc,
                                                    pole_address=poleAddress,light_no=lights('$.lightNo'),light_name=lights('$.lightName'))
                else:
                    sql = "select * from device_pole where pole_id = '%s'" % resp.data
                    return self.checkdb.checkFields(sql, 'hoolink_device', project_id=projectId, area_id=areaId,
                                                    pole_name=poleName,pole_no=poleNo,
                                                    pole_desc=poleDesc,pole_address=poleAddress)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_createWorkOrder(self,resp,projectId,workorderContent,workorderFaultType,workorderLevel,workorderType,workorderAccendantId):
        """
        """
        Logger = Trace("CheckResult::check_createWorkOrder")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_omc', table='workorder',
                                            criteria={"select": "*", "where": "workorder_id=%s" % resp.data}, project_id=projectId, workorder_content=workorderContent,
                                            workorder_fault_type=workorderFaultType, workorder_level=workorderLevel,
                                            workorder_type=workorderType, workorder_accendant_id=workorderAccendantId)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    @logging("CheckResult", "check_updateExternal")
    def check_updateExternal(self,resp,projectId,deviceType,externalName,macAddress):
        """
        """
        if self.__dealwithDeviceResp__(resp):
            return self.__checkByRecord(db='hoolink_device', table='external_device',
                                        criteria={"select": "project_id,device_type,external_name,mac_address",
                                                  "where": "external_id=%s" % resp.data},
                                        project_id=projectId, device_type=deviceType,
                                        external_name=externalName,mac_address='0000'+ str(hex(eval(macAddress))).upper().split('0X')[1])
        return False

    @logging("CheckResult", "check_createLight")
    def check_createLight(self,resp,externalId,lightMacAddress,lightName,lightNo,lightDesc):
        """
        """
        if self.__dealwithDeviceResp__(resp):
            lightId = resp.data
            return self.__checkByRecord(db='hoolink_device', table='device_light',
                                        criteria={"select": "*",
                                                  "where": "light_id=%s" % lightId},
                                        light_desc=lightDesc, external_id=externalId,
                                        light_name=lightName,
                                        light_no=lightNo,
                                        light_mac_address=lightMacAddress,
                                        # light_status=data.lightStatus,enabled=data.enabled
                                        )
        return False

    @logging("CheckResult", "check_deleteNfc")
    def check_deleteNfc(self,resp,nfcId):
        """
        """
        if self.__dealwithDeviceResp__(resp):
            return self.__checkByRecord(db='hoolink_device', table='device_nfc',
                                        criteria={"select": "enabled", "where":"nfc_id=%s"%nfcId},
                                        enabled=0)
        return False


    def check_createNfc(self,resp,nfcNo,poleId,nfcDesc):
        """
        """
        Logger = Trace("CheckResult::check_createNfc")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_device', table='device_nfc',
                                            criteria={"select": "nfc_no,pole_id,nfc_desc", "where":"nfc_id=%s"%resp.data},
                                            nfc_no=nfcNo, pole_id=poleId,
                                            nfc_desc=nfcDesc)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_deleteEnvironment(self,resp):
        """
        """
        Logger = Trace("CheckResult::check_deleteEnvironment")
        try:
            if self.__dealwithDeviceResp__(resp):
                # return self.__existByRecord(db='hoolink_device', table='device_environment',params={"environment_id":resp.data})
                return self.__checkByRecord(db='hoolink_device', table='device_environment',
                                            criteria={"select": "enabled", "where": "environment_id=%s" % resp.data},
                                            enabled=0)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_createEnvironment(self,resp,environmentIp,environmentNo,poleId,environmentDesc):
        """
        """
        Logger = Trace("CheckResult::check_createEnvironment")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_device', table='device_environment',
                                            criteria={"select": "environment_ip,environment_no,pole_id,environment_desc", "where":"environment_id=%s"%resp.data},
                                            environment_ip=environmentIp, environment_no=environmentNo,pole_id=poleId,
                                            environment_desc=environmentDesc)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_createCall(self,resp,callCode,poleId,callDesc):
        """
        """
        Logger = Trace("CheckResult::check_createCall")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_device', table='device_call',
                                            criteria={"select": "call_code,pole_id,call_desc", "where":"call_id=%s"%resp.data},
                                            call_code=callCode, pole_id=poleId,
                                            call_desc=callDesc)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_deleteCall(self,resp,callId):
        """
        """
        Logger = Trace("CheckResult::check_deleteCall")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_device', table='device_call',
                                            criteria={"select": "enabled", "where":"call_id=%s"%callId},
                                            enabled=0)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_createBroadcast(self,resp,broadcastIp,poleId,broadcastDesc):
        """
        """
        Logger = Trace("CheckResult::check_createBroadcast")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_device', table='device_broadcast',
                                            criteria={"select": "broadcast_ip,pole_id,broadcast_desc", "where":"broadcast_id=%s"%resp.data},
                                            broadcast_ip=broadcastIp, pole_id=poleId,
                                            broadcast_desc=broadcastDesc)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_deleteBroadcast(self,resp,broadcastId):
        """
        """
        Logger = Trace("CheckResult::check_deleteBroadcast")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_device', table='device_broadcast',
                                            criteria={"select": "enabled", "where":"broadcast_id=%s"%broadcastId},
                                            enabled=0)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_createScreen(self,resp,screenIp,poleId,screenDesc):
        """
        """
        Logger = Trace("CheckResult::check_createScreen")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_device', table='device_screen',
                                            criteria={"select": "screen_ip,pole_id,screen_desc",
                                                      "where": "screen_id=%s" % resp.data},
                                            screen_ip=screenIp, pole_id=poleId,
                                            screen_desc=screenDesc)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_deleteSceen(self,resp,screenId):
        """
        """
        Logger = Trace("CheckResult::check_deleteSceen")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_device', table='device_screen',
                                            criteria={"select": "enabled", "where":"screen_id=%s"%screenId},
                                            enabled=0)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_deleteCamera(self,resp,cameraId):
        """
        """
        Logger = Trace("CheckResult::check_deleteCamera")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_device', table='device_camera',
                                            criteria={"select": "enabled", "where":"camera_id=%s"%cameraId},
                                            enabled=0)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_createCamera(self,resp,cameraIp,poleId,cameraDesc):
        """
        """
        Logger = Trace("CheckResult::check_createCamera")
        try:
            if self.__dealwithDeviceResp__(resp):
                return self.__checkByRecord(db='hoolink_device', table='device_camera',
                                            criteria={"select": "camera_ip,pole_id,camera_desc", "where":"camera_id=%s"%resp.data},
                                            camera_ip=cameraIp, pole_id=poleId,
                                            camera_desc=cameraDesc)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_addReturnAddress(self,resp):
        """
        """
        Logger = Trace("CheckResult::check_addReturnAddress")
        try:
            resp = self.__dealwithGatewayResp__(resp)
            if resp is not None:
                # if self.__checkByField(schma='tradelogistics',table='TradeAddress',fieldkey='addressId',fieldvalue=resp.addressId,userId=resp.userId):
                #     return self.__deleteByField('tradelogistics','TradeAddress','addressId',resp.addressId)
                if self.__checkByRecord(db='tradelogistics',table='TradeAddress',criteria={"select":"userId","where":"addressId=%s"%resp.addressId},userId=resp.userId):
                    return self.__deleteByRecord(db='tradelogistics',table='TradeAddress',params={"addressId":resp.addressId})
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False


    def check_readFileById(self,resp):
        """
        """
        Logger = Trace("CheckResult::check_readFileById")
        try:
            if self.__dealwithDeviceResp__(resp):
                Enable = 1 if resp.data.userEnableStr == u'启用' else 0
                return self.__checkByRecord(db='hoolink_ability', table='ability_file',
                                            criteria={"select": "*", "where":"file_id=%s"%resp.data.fileId},
                                            file_path=resp.data.filePath, file_name=resp.data.fileName,enable=Enable,
                                            group_id=resp.data.groupId,file_ip_addr=resp.data.fileIpAddr)
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def check_createOrderActionlet(self,resp):
        """
        """
        Logger = Trace("CheckResult::check_createOrderActionlet")
        try:
            resp = self.__dealwithGatewayResp__(resp)
            if resp is not None:
                # schma = caculateSchemaName("xdtrade", shopOrderId)
                # tablename = caculateTableName(shopOrderId)
                if self.__updateByRecord(db='tradelogistics',table='TradeAddress',criteria={"select":"userId","where":"addressId=%s"%resp.addressId},userId=resp.userId):
                    return self.__deleteByRecord(db='tradelogistics',table='TradeAddress',params={"addressId":resp.addressId})
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

if __name__ == '__main__':
    records = [{'project_area_name': u'02680302032', 'project_area_desc': u'15407353844'}]
    records = JSONProcessor({'records':records})
    projectAreaName = '02680302032' #第一个字符不能为0
    projectAreaDesc = '15407353844'
    if (projectAreaName in records(
            '$..*[@.project_area_name is %s].project_area_name' % projectAreaName) and projectAreaDesc in records(
            '$..*[@.project_area_desc is %s].project_area_desc' % projectAreaDesc)):
        print 'yes'
    else:
        print 'no'