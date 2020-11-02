#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
import mysql.connector
import mysql.connector.errors
import sys
from fs.Trace import Trace
reload(sys)
sys.setdefaultencoding('utf-8') 

class Const(object):
    PICT_PARAMS = "d:/params.txt" # 请求参数存放地址txt
    PICT_PARAMS_RESULT = "d:/t2.txt" # 参数配对后的路径excel
    HTTP_POST = "post"
    HTTP_GET = "get"

    # 数据库的常用字段
    FIND_BY_SQL = "findBySql" # 根据sql查找
    COUNT_BY_SQL = "countBySql" # 自定义sql 统计影响行数
    INSERT = "insert" # 插入
    UPDATE_BY_ATTR = "updateByAttr" # 更新数据
    DELETE_BY_ATTR = "deleteByAttr" # 删除数据
    FIND_BY_ATTR = "findByAttr" # 根据条件查询一条记录
    FIND_ALL_BY_ATTR = "findAllByAttr"  #根据条件查询多条记录
    COUNT = "count" # 统计行
    EXIST = "exist" # 是否存在该记录

class MySQLet:
    """Connection to a MySQL"""
    def __init__(self,**kwargs):
        try:
            self._conn = mysql.connector.connect(host=kwargs["host"], user=kwargs["user"], password=kwargs["password"],
                                                 charset=kwargs["charset"], database=kwargs["database"], port=kwargs["port"])
            self.__cursor = None
            print("连接数据库")
            #set charset charset = ('latin1','latin1_general_ci')
        except mysql.connector.errors.ProgrammingError as err:
            print('mysql连接错误：' + err.msg)

    # def findBySql(self, sql, params={}, limit=0, join='AND'):
    def findBySql(self, **kwargs):
        """
        自定义sql语句查找
        limit = 是否需要返回多少行
        params = dict(field=value)
        join = 'AND | OR'
        """
        print("-----------findbysql-----")
        # print(kwargs)
        cursor = self.__getCursor()
        # sql = self.__joinWhere(kwargs["sql"], kwargs["params"], kwargs["join"])
        if kwargs.get("join", 0) == 0: kwargs["join"] = "AND"
        if kwargs.get("limit", "0") == "0": kwargs["limit"] = 1
        sql = self.__joinWhere(**kwargs)
        # print 'sql = %s,params = %s' %(sql,tuple(kwargs["params"].values()))
        cursor.execute(sql, tuple(kwargs["params"].values()))
        rows = cursor.fetchmany(size=kwargs["limit"]) if kwargs["limit"] > 0 else cursor.fetchall()
        result = [dict(zip(cursor.column_names,row)) for row in rows] if rows else None
        return result

    # def countBySql(self,sql,params = {},join = 'AND'):
    def countBySql(self, **kwargs):
        """自定义sql 统计影响行数"""
        if kwargs.get("join", 0) == 0: kwargs["join"] = "AND"
        cursor = self.__getCursor()
        # sql = self.__joinWhere(kwargs["sql"], kwargs["params"], kwargs["join"])
        sql = self.__joinWhere(**kwargs)
        cursor.execute(sql, tuple(kwargs["params"].values()))
        result = cursor.fetchall() # fetchone是一条记录， fetchall 所有记录
        return len(result) if result else 0

    # def insert(self,table,data):
    def insert(self, **kwargs):
        """新增一条记录
          table: 表名
          data: dict 插入的数据
        """
        fields = ','.join('`'+k+'`' for k in kwargs["data"].keys())
        values = ','.join(("%s", ) * len(kwargs["data"]))
        sql = 'INSERT INTO `%s` (%s) VALUES (%s)' % (kwargs["table"], fields, values)
        cursor = self.__getCursor()
        cursor.execute(sql, tuple(kwargs["data"].values()))
        insert_id = cursor.lastrowid
        self._conn.commit()
        return insert_id

    # def updateByAttr(self,table,data,params={},join='AND'):
    def updateByAttr(self, **kwargs):
    #     """更新数据"""
        if kwargs.get("params", 0) == 0:
            kwargs["params"] = {}
        if kwargs.get("join", 0) == 0:
            kwargs["join"] = "AND"
        fields = ','.join('`' + k + '`=%s' for k in kwargs["data"].keys())
        values = list(kwargs["data"].values())


        values.extend(list(kwargs["params"].values()))
        sql = "UPDATE `%s` SET %s " % (kwargs["table"], fields)
        kwargs["sql"] = sql
        sql = self.__joinWhere(**kwargs)
        print sql
        cursor = self.__getCursor()
        print values
        cursor.execute(sql, tuple(values))
        self._conn.commit()
        return cursor.rowcount


    # def updateByPk(self,table,data,id,pk='id'):
    def updateByPk(self, **kwargs):
        """根据主键更新，默认是id为主键"""
        return self.updateByAttr(**kwargs)

    # def deleteByAttr(self,table,params={},join='AND'):
    def deleteByAttr(self, **kwargs):
        """删除数据"""
        if kwargs.get("params", 0) == 0:
            kwargs["params"] = {}
        if kwargs.get("join", 0) == 0:
            kwargs["join"] = "AND"
        # fields = ','.join('`'+k+'`=%s' for k in kwargs["params"].keys())
        sql = "DELETE FROM `%s` " % kwargs["table"]
        kwargs["sql"] = sql
        # sql = self.__joinWhere(sql, kwargs["params"], kwargs["join"])
        sql = self.__joinWhere(**kwargs)
        # print 'sql = %s , kwargs["params"].values()=%s'%(sql,repr(kwargs["params"].values()))
        cursor = self.__getCursor()
        cursor.execute(sql, tuple(kwargs["params"].values()))
        self._conn.commit()
        return cursor.rowcount

    # def deleteByPk(self,table,id,pk='id'):
    def deleteByPk(self, **kwargs):
        """根据主键删除，默认是id为主键"""
        return self.deleteByAttr(**kwargs)

    # def findByAttr(self,table,criteria = {}):
    def findByAttr(self, **kwargs):
        """根據條件查找一條記錄"""
        return self.__query(**kwargs)

    # def findByPk(self,table,id,pk='id'):
    def findByPk(self, **kwargs):
        return self.findByAttr(**kwargs)

    # def findAllByAttr(self,table,criteria={}, whole=true):
    def findAllByAttr(self, **kwargs):
        """根據條件查找記錄"""
        return self.__query(**kwargs)

    # def count(self,table,params={},join='AND'):
    def count(self, **kwargs):
        """根据条件统计行数"""
        if kwargs.get("join", 0) == 0: kwargs["join"] = "AND"
        sql = 'SELECT COUNT(*) FROM `%s`' % kwargs["table"]
        # sql = self.__joinWhere(sql, kwargs["params"], kwargs["join"])
        kwargs["sql"] = sql
        sql = self.__joinWhere(**kwargs)
        cursor = self.__getCursor()
        cursor.execute(sql, tuple(kwargs["params"].values()))
        result = cursor.fetchone()
        return result[0] if result else 0

    # def exist(self,table,params={},join='AND'):
    def exist(self, **kwargs):
        """判断是否存在"""
        return self.count(**kwargs) > 0

    def close(self):
        """关闭游标和数据库连接"""
        if self.__cursor is not None:
            self.__cursor.close()
        self._conn.close()

    def __getCursor(self):
        """获取游标"""
        if self.__cursor is None:
            self.__cursor = self._conn.cursor()
        return self.__cursor

    # def __joinWhere(self,sql,params,join):
    def __joinWhere(self, **kwargs):
        """转换params为where连接语句"""
        # print 'kwargs = %s'%kwargs
        if kwargs["params"]:
            keys,_keys = self.__tParams(**kwargs)
            where = ' AND '.join(k+'='+_k for k,_k in zip(keys,_keys)) if kwargs["join"] == 'AND' else ' OR '.join(k+'='+_k for k,_k in zip(keys,_keys))
            kwargs["sql"]+=' WHERE ' + where
        return kwargs["sql"]

    # def __tParams(self,params):
    def __tParams(self, **kwargs):
        keys = ['`'+k+'`' for k in kwargs["params"].keys()]
        _keys = ['%s' for k in kwargs["params"].keys()]
        return keys,_keys

    # def __query(self,table,criteria,whole=False):
    def __query(self, **kwargs):
        # print 'kwargs = %s'%kwargs
        if kwargs.get("whole", False) == False or kwargs["whole"] is not True:
            kwargs["whole"] = False
            kwargs["criteria"]['limit'] = 1
        # sql = self.__contact_sql(kwargs["table"], kwargs["criteria"])
        sql = self.__contact_sql(**kwargs)
        cursor = self.__getCursor()
        cursor.execute(sql)
        rows = cursor.fetchall() if kwargs["whole"] else cursor.fetchone()
        result = [dict(zip(cursor.column_names, row)) for row in rows] if kwargs["whole"] else dict(zip(cursor.column_names, rows)) if rows else None
        return result

    # def __contact_sql(self,table,criteria):
    def __contact_sql(self, **kwargs):
        logger = Trace('__contact_sql')
        # logger.debug('kwargs = %s'%kwargs)
        sql = 'SELECT '
        if kwargs["criteria"] and type(kwargs["criteria"]) is dict:
            #select fields
            if 'select' in kwargs["criteria"]:
                fields = kwargs["criteria"]['select'].split(',')
                sql+= ','.join('`'+field+'`' for field in fields)
            else:
                sql+=' * '
            #table
            sql+=' FROM `%s`'% kwargs["table"]
            #where
            if 'where' in kwargs["criteria"]:
                sql+=' WHERE '+ kwargs["criteria"]['where']
            #group by
            if 'group' in kwargs["criteria"]:
                sql+=' GROUP BY '+ kwargs["criteria"]['group']
            #having
            if 'having' in kwargs["criteria"]:
                sql+=' HAVING '+ kwargs["criteria"]['having']
            #order by
            if 'order' in kwargs["criteria"]:
                sql+=' ORDER BY '+ kwargs["criteria"]['order']
            #limit
            if 'limit' in kwargs["criteria"]:
                sql+=' LIMIT '+ str(kwargs["criteria"]['limit'])
            #offset
            if 'offset' in kwargs["criteria"]:
                sql+=' OFFSET '+ str(kwargs["criteria"]['offset'])
        else:
            sql+=' * FROM `%s`'% kwargs["table"]
        logger.debug('sql = %s , kwargs = %s'%(sql,kwargs))
        return sql

    def findKeySql(self, key ,**kwargs):
        sqlOperate = {
        Const.COUNT: lambda: self.count(**kwargs),
        Const.COUNT_BY_SQL: lambda: self.countBySql(**kwargs),
        Const.DELETE_BY_ATTR: lambda: self.deleteByAttr(**kwargs),
        Const.EXIST: lambda: self.exist(**kwargs),
        Const.FIND_ALL_BY_ATTR: lambda: self.findAllByAttr(**kwargs),
        Const.INSERT: lambda: self.insert(**kwargs),
        Const.FIND_BY_ATTR: lambda: self.findByAttr(**kwargs),
        Const.UPDATE_BY_ATTR: lambda: self.updateByAttr(**kwargs),
        Const.FIND_BY_SQL: lambda: self.findBySql(**kwargs)

        }
        return sqlOperate[key]()