#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on June 01, 2019
@author: hzhuangfg
di san ci xiugai
'''

import sys
import os
import time
import logging
import logging.handlers
import StringIO
import datetime
from logging.handlers import RotatingFileHandler
from Config import *

_log_dir=os.path.normpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
TRACE_FILE_NAME = "trace.%s.log"%(str(datetime.datetime.now().strftime('%Y-%m-%d')))

print "os.getcwd() = %s" %os.getcwd()
print "os.path.dirname(__file__) = %s" %os.path.dirname(__file__)
print "_log_dir = %s" % _log_dir

_log_path=os.path.join(_log_dir, '..//logs')
if not os.path.exists(os.path.normpath(_log_path)):
    os.makedirs(_log_path)
_log_path=os.path.normpath(os.path.join(_log_path, TRACE_FILE_NAME))


#=============================================================================
#Singleton_Base
class Singleton_Base(type):
    """Singleton Metaclass"""

    def __init__(cls, name, bases, dic):
        super(Singleton_Base, cls).__init__(name, bases, dic)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton_Base, cls).__call__(*args, **kwargs)
        return cls.instance

#=============================================================================

#=============================================================================
class Log:
    __metaclass__ = Singleton_Base
    def __init__(self, logpath=""):
        """
        """
        try:
            self.logger = logging.getLogger()
            self.handle = None
            LOG_MODE = 'a'
            b_exist=False
            for handle in self.logger.handlers:
                if False == isinstance(handle, logging.FileHandler):
                    print("Log::__init__ handle", type(handle), handle)
                    continue
                
                if logpath == handle.baseFilename:
                    b_exist=True
                else:
                    print("GGG", handle.baseFilename, logpath)

            if False == b_exist:
                if os.path.exists(os.path.dirname(logpath)):
                    #self.handle = logging.FileHandler(logpath) #, mode="w+"
                    self.handle = RotatingFileHandler(logpath, LOG_MODE, LOG_MAX_SIZE, LOG_MAX_FILES)
                    self.logger.addHandler(self.handle)
                    print("Log.__init__ file mode", self.logger.handlers)
                else:
                    #self.handle = logging.StreamHandler()
                    self.handle = RotatingFileHandler(logpath, LOG_MODE, LOG_MAX_SIZE, LOG_MAX_FILES)
                    self.logger.addHandler(self.handle)
                    print("Log.__init__ stdout mode")
            
        except Exception, e:
            print("Log.__init__", e)
    
    
    def __del__(self):
        """
        """
        try:
            self.__close__()
        except Exception, e:
            print("Log.__del__", e)
    
    
    def __format__(self, *args):
        output = StringIO.StringIO()
        try:
            if 1 == len(args) :
                output.write(args[0])
            else:
                output.write(' '.join(args))
                # output.write("%s %s: " %(args[0],args[1:]))
                # output.write(args)
            
            ret_str = output.getvalue()
            output.close()
            return ret_str
        except Exception, e:
            output.write("Exception: ")
            output.write(e)
            ret_str = output.getvalue()
            output.close()
            return ret_str
    
    
    def __close__(self):
        try:
            if type(None) != type(self.handle):
                self.logger.removeHandler(self.handle)
                self.handle.close()
                self.handle=None
                self.logger=None
        except Exception, e:
            print("Log::__close__", e)
            return False
    
    
    def debug(self, *args):
        try:
            fargs = "debug:: " + self.__format__(*args)
            self.logger.debug(fargs)
            # print(fargs)
            return True
        except Exception, e:
            self.logger.error(e)
            return False
    
    
    def info(self, *args):
        try:
            fargs = "info:: " + self.__format__(*args)
            self.logger.info(fargs)
            # print(fargs)
            return True
        except Exception, e:
            self.logger.error(e)
            return False
    
    
    def warn(self, *args):
        try:
            fargs = "warn:: " + self.__format__(*args)
            self.logger.warn(fargs)
            # print(fargs)
            return True
        except Exception, e:
            self.logger.error(e)
            return False
    
    
    def error(self, *args):
        try:
            fargs = "error:: " + self.__format__(*args)
            self.logger.error(fargs)
            # print(fargs)
            return True
        except Exception, e:
            self.logger.error(e)
            return False
    
    
    def critical(self, *args):
        try:
            fargs = "critical:: " + self.__format__(*args)
            self.logger.critical(fargs)
            # print(fargs)
            return True
        except Exception, e:
            self.logger.error(e)
            return False
    
    
    def setLevel(self, level):
        try:
            #check parameters
            level_dict={0: "NOSET", 10: "DEBUG", 20: "INFO", 30: "WARNNING", 40: "ERROR", 50: "CRITICAL"}
            if level not in level_dict:
                raise Exception("error input, level must be %s" %("0 | 10 | 20 | 30 | 40 | 50"))
            
            self.logger.setLevel(level)
            return True
        except Exception, e:
            print(e)
            return False
    
    
#=============================================================================


#=============================================================================
class Trace:
    def __init__(self, func_name=""):
        try:
            self.log=Log(_log_path)
            
            if type(None) != self.log:
                self.log.setLevel(0)
                self.func_name=func_name
                self.__onEnter__()
        except Exception, e:
            print("Trace::__init__", e)
    
    
    def __del__(self):
        try:
            if type(None) != self.log:
                self.__onLeave__()
                self.log=None
        except Exception, e:
            print("Trace::__del__", e)
    
    
    def __onEnter__(self):
        try:
            self.log.info("%s Enter %s"  %(str(datetime.datetime.now()),self.func_name))
        except Exception, e:
            self.log.error("%s Enter %s"  %(str(datetime.datetime.now()),self.func_name), e)
    
    
    def __onLeave__(self):
        try:
            self.log.info( "%s Leave %s" %(str(datetime.datetime.now()),self.func_name ))
        except Exception, e:
            self.log.error("%s Leave %s" %(str(datetime.datetime.now()),self.func_name), e)
    
    def __format__(self, *args):
        output = StringIO.StringIO()
        try:
            output.write("%s %s: " %(str(datetime.datetime.now()),self.func_name))
            if 1 == len(args) :
                output.write(args[0])
            else:
                # output.write(args)
                # output.write("%s %s " %(args[0],args[1]))
                output.write(' '.join(args))
            
            ret_str = output.getvalue()
            output.close()
            return ret_str
        except Exception, e:
            output.write("Exception %s: " %(self.func_name))
            output.write(e)
            ret_str = output.getvalue()
            output.close()
            return ret_str
    
    
    def debug(self, *args):
        try:
            fargs = self.__format__(*args)
            self.log.debug(fargs)
        except Exception,e:
            self.log.error(e)
    
    
    def info(self, *args):
        try:
            fargs = self.__format__(*args)
            self.log.info(fargs)
        except Exception,e:
            self.log.error(e)
    
    
    def warn(self, *args):
        try:
            fargs = self.__format__(*args)
            self.log.warn(fargs)
        except Exception,e:
            self.log.error(e)
    
    
    def error(self, *args):
        try:
            fargs = self.__format__(*args)
            self.log.error(fargs)
        except Exception,e:
            self.log.error(e)
    
    
    def critical(self, *args):
        try:
            fargs = self.__format__(*args)
            self.log.critical(fargs)
        except Exception,e:
            self.log.error(e)
    
    
#============================================================================= 



