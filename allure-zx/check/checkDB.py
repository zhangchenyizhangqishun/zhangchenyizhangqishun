#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on July 12, 2019
@author: hzhuangfg
di si ci tijiao
'''
import Config
from com.util import gen_md5_sign
from engine.db import MySQLet,Const
from fs.Trace import Trace
from com.mysql import *
from com.json_processor import JSONProcessor
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式

class CheckDB():
    def __init__(self,logId,env = 'test'):
        self.env = env
        self.logId = gen_md5_sign(logId)

    def __getRecordBySql(self,sql,dbname):
        """
        返回数据库信息
        :param sql:
        :param dbname:
        :return:
        """
        Logger = Trace("CheckDB::__getRecordBySql")
        try:
            conn = connectDB(Config.dbhost, Config.dbport, Config.dbuser, Config.dbpass, dbname)
            data = queryDB(conn, sql)
            conn.close()
            if data:
                return JSONProcessor(data[0])
            return None
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error("error: %s" % errMsg)
            return None


    def __getRecordsBySql(self,sql,dbname):
        """
        返回数据库信息
        :param sql:
        :param dbname:
        :return:
        """
        Logger = Trace("CheckDB::__getRecordsBySql")
        try:
            conn = connectDB(Config.dbhost, Config.dbport, Config.dbuser, Config.dbpass, dbname)
            data = queryDB(conn, sql)
            conn.close()
            if data:
                return data
                # return JSONProcessor(data[0])
            return None
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error("error: %s" % errMsg)
            return None

    def __getRecord(self,db,table,**criteria):
        """
        返回数据库记录
        :param db:
        :param table:
        :param criteria:
        :return:
        """
        Logger = Trace("CheckDB::__getRecord")
        try:
            mysqlet = MySQLet(host=Config.dbhost, user=Config.dbuser, password=Config.dbpass, charset="utf8",
                              database=db, port=Config.dbport)
            data = mysqlet.findKeySql(Const.FIND_BY_ATTR, table=table,criteria=criteria)
            # Logger.info('criteria = %s ,data = %s'%(repr(criteria),data))
            if data:
                """
                u'project_lat': Decimal('23.699277000000') --> TypeError: Decimal('23.699277000000') is not JSON serializable
                """
                # return JSONProcessor(data)
                return data
            return None
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error("error: %s" % errMsg)
            return None


    def __recordExist(self,db,table,**params):
        """
        判断数据库记录是否存在
        :param db:
        :param table:
        :param params:
        :return:
        """
        Logger = Trace("CheckDB::__recordExist")
        try:
            mysqlet = MySQLet(host=Config.dbhost, user=Config.dbuser, password=Config.dbpass, charset="utf8",
                              database=db, port=Config.dbport)
            return mysqlet.findKeySql(Const.EXIST, table=table,**params)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error("error: %s" % errMsg)
            return False

    def __deleteRecord(self,db,table,**params):
        """
        删除数据库记录
        :param db:
        :param table:
        :param params:
        :return:
        """
        Logger = Trace("CheckDB::__deleteRecord")
        try:
            mysqlet = MySQLet(host=Config.dbhost, user=Config.dbuser, password=Config.dbpass, charset="utf8",
                              database=db, port=Config.dbport)
            return mysqlet.findKeySql(Const.DELETE_BY_ATTR, table=table, **params)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error("error: %s" % errMsg)
            return None

    def __updateRecord(self,db,table,**params):
        """
        更新数据库记录
        :param db:
        :param table:
        :param params:
        :return:
        """
        Logger = Trace("CheckDB::__updateRecord")
        try:
            mysqlet = MySQLet(host=Config.dbhost, user=Config.dbuser, password=Config.dbpass, charset="utf8",
                              database=db, port=Config.dbport)
            return mysqlet.findKeySql(Const.UPDATE_BY_ATTR, table=table, **params)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error("error: %s" % errMsg)

    def __printRecord(self,db,table,**criteria):
        """
        打印记录字段
        :param db:
        :param table:
        :param criteria:
        :return:
        """
        Logger = Trace("CheckDB::__printRecord")
        try:
            record = self.__getRecord(db,table,**criteria)
            if record is not None:
                for key,value in record.iteritems():
                    Logger.debug('%s: %s'%(key,value))
                return record
            return None
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error("error: %s" % errMsg)
            return None

    def printRecord(self,db,table,**kwargs):
        """
        打印记录字段
        :param db:
        :param table:
        :param criteria:
        :return:
        """
        Logger = Trace("CheckDB::printRecord")
        try:
            criteria = kwargs.get('criteria', None)
            return self.__printRecord(db,table,**criteria)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error("error: %s" % errMsg)
            return None

    def checkRecord(self,db,table,**kwargs):
        """
        校验查询记录字段是否满足预期
        :param db:
        :param table:
        :param kwargs:
                    查询条件：criteria={"select":"userId","where":"addressId=400011241"},
                    校验字段：userId="93106308"
        :return:
        """
        Logger = Trace("CheckDB::checkRecord")
        try:
            criteria = kwargs.get('criteria',None)
            if criteria is not None:
                del kwargs['criteria']  #校验不需要带查询条件
                record = self.__printRecord(db,table,**criteria)
                if record is not None:
                    for key, value in kwargs.items():
                        Logger.debug('record.key = %s , record.value = %s' % (key, record[key]))
                        if value == [] or value == {} or value == ():   #
                            value = None
                        if record[key] != value:
                            if str(value).find(str(record[key])) == -1 and str(record[key]).find(str(value)) == -1:
                                Logger.critical('expect.type = %s value = %s , record.type = %s value = %s' % (
                                    type(str(value)), str(value), type(str(record[key])), str(record[key])))
                                return False
                        # Logger.debug('record.key = %s , record.value = %s'%(key,record[key]))
                        # if record[key] != value:
                        #     Logger.critical('expect.value = %s , record.value = %s'%(value,record[key]))
                        #     return False
                    return True
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def __updateRecordBySql(self,sql,db_name):
        """
        更新数据库
        :param sql:
        :param db_name:
        :return:
        """
        Logger = Trace("CheckDB::__updateRecordBySql")
        try:
            conn = connectDB(Config.dbhost, Config.dbport, Config.dbuser, Config.dbpass, db_name)
            executeSQL(conn, sql)
            conn.close()
            return True
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error("error: %s" % errMsg)
            return False

    def __printRecordBySql(self,sql,db_name):
        """
        :param sql:
        :param db_name:
        :return:
        """
        Logger = Trace("CheckDB::__printRecordBySql")
        try:
            record = self.__getRecordBySql(sql,db_name)
            if record is not None:
                for key,value in record.iteritems():
                    Logger.debug('%s: %s'%(key,value))
                return record
            return None
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error("error: %s" % errMsg)
            return None

    def __printRecordsBySql(self,sql,db_name):
        """
        :param sql:
        :param db_name:
        :return:
        """
        Logger = Trace("CheckDB::__printRecordsBySql")
        try:
            records = self.__getRecordsBySql(sql,db_name)
            Logger.debug('sql = %s'%sql)
            if records:
                # for record in records:
                #     if record is not None:
                #         for key,value in record.iteritems():
                #             Logger.debug('%s: %s'%(key,value))
                return records
            return None
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error("error: %s" % errMsg)
            return None

    def checkField(self,sql,db_name,**kwargs):
        """
        """
        Logger = Trace("CheckDB::checkField")
        try:
            record = self.__printRecordBySql(sql,db_name)
            if record is not None:
                for key, value in kwargs.items():
                    Logger.debug('record.key = %s , record.value = %s'%(key,record[key]))
                    if value == [] or value == {} or value == ():
                        value = None
                    if record[key] != value:
                        if str(value).find(str(record[key])) == -1:
                            Logger.critical('expect.type = %s value = %s , record.type = %s value = %s' % (
                            type(str(value)), str(value), type(str(record[key])), str(record[key])))
                            return False
                return True
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def checkFields(self,sql,db_name,**kwargs):
        """
        """
        Logger = Trace("CheckDB::checkFields")
        try:
            records = self.__printRecordsBySql(sql,db_name)
            if records is not None:
                for record in records:
                    for key, value in kwargs.items():
                        # Logger.debug('record.key = %s , record.value = %s , expaect.value = %s'%(key,record[key],value))
                        if value == [] or value == {} or value == () or value == '':
                            value = None
                        if record[key] != value:
                            if str(value).find(str(record[key])) == -1:
                                Logger.critical('key = %s ,expect.type = %s value = %s , record.type = %s value = %s' % (key,
                                type(str(value)), str(value), type(str(record[key])), str(record[key])))
                                return False
                return True
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def checkFieldByFilter(self,record,**kwargs):
        """
        """
        Logger = Trace("CheckDB::checkFieldByFilter")
        try:
            # record = self.__printRecordBySql(sql,db_name)
            if record is not None:
                for key, value in kwargs.items():
                    Logger.info('record.key = %s , record.value = %s'%(key,record[key]))
                    if record[key] != value:
                        return False
                return True
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def updateByField(self,sql,db_name):
        """
        """
        Logger = Trace("CheckDB::updateByField")
        try:
            return self.__updateRecordBySql(sql,db_name)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def deleteByRecord(self,db,table,**params):
        """
        """
        Logger = Trace("CheckDB::deleteByRecord")
        try:
            return self.__deleteRecord(db,table,**params)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def existByRecord(self,db,table,**params):
        """
        """
        Logger = Trace("CheckDB::existByRecord")
        try:
            return self.__recordExist(db,table,**params)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def updateByRecord(self,db,table,**params):
        """
        """
        Logger = Trace("CheckDB::updateByRecord")
        try:
            return self.__updateRecord(db,table,**params)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False

    def getField(self,sql,db_name,*args):
        """
        """
        Logger = Trace("CheckDB::getField")
        try:
            record = self.__printRecordBySql(sql,db_name)
            field = {}
            if record is not None:
                for key in args:
                    Logger.debug('record.key = %s , record.value = %s'%(key,record[key]))
                    if record.has_key(key):
                        field[key] = record[key]
                return JSONProcessor(record)
            return None
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return None


    def getFields(self,sql,db_name):
        """
        """
        Logger = Trace("CheckDB::getField")
        try:
            records = self.__printRecordsBySql(sql,db_name)
            return records
            # field = {}
            # if record is not None:
            #     # for key in args:
            #     #     Logger.debug('record.key = %s , record.value = %s'%(key,record[key]))
            #     #     if record.has_key(key):
            #     #         field[key] = record[key]
            #     return JSONProcessor(record)
            # return None
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return None
