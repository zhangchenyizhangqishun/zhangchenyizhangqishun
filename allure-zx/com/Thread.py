#!/usr/bin/env python
# _*_ coding:UTF-8

'''
Created on June 16, 2019
@author: hzhuangfg
多线程处理
'''

import threading
import time
from fs.Trace import Trace

class test_Thread(threading.Thread):
    def __init__(self,func,args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.ret_flag = []

    def __call__(self):
        apply(self.func,self.args)

    def trace_func(self, func, *args):
        """
        @note:替代profile_func，新的跟踪线程返回值的函数，对真正执行的线程函数包一次函数，以获取返回值
        """
        Logger = Trace("test_Thread::trace_func")
        ret = func(*args)
        Logger.info('ret == ',ret)
        self.ret_flag.append(ret)
