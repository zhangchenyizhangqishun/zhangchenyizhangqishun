#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
Created on June 16, 2019
@author: hzhuangfg
'''
import MySQLdb
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式

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

def executeSQL(conn, sql):
    cursor = conn.cursor()
    try:
        print "Run SQL: %s" % sql
        cursor.execute(sql)
        conn.commit()
        print "Rows updated:", cursor.rowcount
      # 发生错误时回滚
    except Exception, e:
        errMsg = traceback.format_exc()
        print("error: %s" % errMsg)
        conn.rollback()
    cursor.close()
