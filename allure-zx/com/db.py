#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
Created on May 26, 2019
@author: hzhuangfg
'''
import MySQLdb
import traceback
from functools import wraps
from com.json_processor import JSONProcessor
import sys

class Configuraion:
    def __init__(self, env):
        if env == "Prod":
            self.host = "10.7.13.48"
            self.port = 8066
            self.user = "admin"
            self.passwd = "9MeRMf7b15SvsjLpQFtB"
        elif env == "Test":
            self.host = "10.7.13.48"
            self.port = 8066
            self.user = "admin"
            self.passwd = "9MeRMf7b15SvsjLpQFtB"

def mysql_querydb():
    _conf = Configuraion(env="Test")
    def connectDB(dbhost, dbport, dbuser, dbpass, dbname):
        conn = MySQLdb.connect(host=dbhost, port=dbport, user=dbuser, passwd=dbpass, db=dbname,charset='utf8')
        return conn

    def queryDB(conn, sql):
        print "Run SQL: %s" % sql
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)
        print "Rows selected:", cursor.rowcount
        data = []
        for row in cursor.fetchall():
            data.append(row)
        cursor.close()
        return data
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            sql = str(args[0])
            dbname = str(args[1])
            conn = connectDB(_conf.host, _conf.port, _conf.user,_conf.passwd,dbname)
            try:
                data = queryDB(conn,sql)
            except Exception, e:
                errMsg = traceback.format_exc()
                print("error: %s" % errMsg)
                data = None
                # sys.exit(1)
            kwargs["data"] = data
            conn.close()
            result = fn(*args, **kwargs)
            # fn(*args, **kwargs)
            return result
        return wrapper
    return decorator

sql = "select * from Bill where businessRecordNumber = '%s'"%(1416121319501110001)
dbname = 'bill'
@mysql_querydb()
def getFromDB(sql,dbname,data):
    print 'sql = %s dbname = %s'%(sql,dbname)
    print 'data = %s'%data
    if data :
        return JSONProcessor(data[0])

