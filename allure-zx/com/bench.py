#! /usr/bin/env python  
# -*- coding: UTF-8 -*-  
'''
Created on  June 12, 2017
@author:hzhuangfg
基础库
'''
import time,threading,random,StringIO
from fs.Trace import Trace
import traceback
from Config import *
import sys,socket
socket.setdefaulttimeout(60)  

class benchmark:
    def __init__(self):
        self.Longest_transaction = 0
        self.Shortest_transaction = 100.0
        self.error_amount = 0
        self.pass_amount = 0
        self.total_amount = 0
        self.total_time = 0
        self.avg_total_time = 0
        self.downloaded = 0
        self.Concurrency = 1
        self.threads_dict = {}
        self.threads_amount = 0
        self.run_time = 200
        self.haveruntime = 0
        self.thread_ret = []            #每个线程返回结果
        self.time_consuming_list = []   #每个事务执行时间


#         self.data= (int(total_amount),                      #执行次数
#                   round(self.Availability*100.0,1),         #成功率
#                   round(self.haveruntime,3),                #总耗时
#                   round(self.downloaded/(1048576.0),3 ),    #数据量(MB)
#                   round(self.Response_time*1000,3),         #响应时间(ms)
#                   round(self.Transaction_rate,3),           #执行率(t/s)
#                   round(self.Throughput,2),                 #吞吐速度(mb/s)
#                   round(self.Concurrency,3),                #并发个数
#                   int(self.pass_amount),                    #成功次数
#                   int(self.total_amount-pass_amount),       #失败次数
#                   round(self.Longest_transaction,2),        #最长响应时间
#                   round(self.Shortest_transaction*1000,2)   #最短响应时间
#               )
#
    def __del__(self):
        del self.thread_ret[:]
        del self.time_consuming_list[:]

    def set_run_time(self,haveruntime,total_time):
        """
        设置执行时间
        :param haveruntime:
        :param total_time:
        :return:
        """
        Logger = Trace("benchmark::set_run_time")
        try:
            self.haveruntime = haveruntime
            self.total_time = total_time
            return True
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error("error = %s"%errMsg)
            return False

    def display_bench(self):
        """
        输出性能参数
        :return:
        """
        Logger = Trace("benchmark::display_bench")
        try:
            self.info = {
                 'Transactions':self.total_amount,
                 'Concurrency':self.Concurrency,
                 'Successful_transactions':self.pass_amount,
                 'Fail_transactions':self.error_amount,
                 'Fail_rate':self.error_amount/self.total_amount,
                 'Longest_transaction':self.Longest_transaction,
                 'Shortest_transaction':self.Shortest_transaction,
                 'Elapsed_time':self.total_time,
                 'Data_transferred':self.downloaded,
                 'Availability':self.pass_amount/self.total_amount,
                 #'Response_time':self.total_time/self.pass_amount,
                 'Response_time':self.avg_total_time/self.total_amount,
                 'Transaction_rate':self.total_amount/self.avg_total_time,
                 'Throughput':self.downloaded/self.haveruntime
                 }
            Logger.info(repr(self.info))
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error("error:%s"%errMsg)

    def statistic_analysis_multi_thread(self):
        """
        分析多线程执行结果
        :return:True or False
        """
        Logger = Trace("benchmark::statistic_analysis_multi_thread")
        try:
            Logger.info('thread_ret = %s'%repr(self.thread_ret))
            ret_fail_count = 0
            for ret in self.thread_ret:
                if ret == False:
                    ret_fail_count += 1

            #统计所有事务最小响应时间和最长响应时间
            for time_consuming in self.time_consuming_list:
                #Logger.info('time_consuming = %s'%time_consuming)
                self.avg_total_time += time_consuming
                if time_consuming > self.Longest_transaction:
                    self.Longest_transaction = time_consuming
                if time_consuming < self.Shortest_transaction:
                    self.Shortest_transaction = time_consuming

            self.pass_amount = float(len(self.thread_ret)-ret_fail_count)
            self.error_amount = float(ret_fail_count)
            self.total_amount = float(len(self.thread_ret))
            self.Concurrency = threading.activeCount() - 1
            self.display_bench()
            rate = float(ret_fail_count)/float(len(self.thread_ret))
            rate_num = rate * 100
            if rate_num > concurrence_fail_rate:
                Logger.info('fail_rate = %f%% ' %(rate_num))
                return False
            return  True
        except Exception, e:
                errMsg = traceback.format_exc()
                Logger.error("error: %s" % errMsg)
                return False

    def trace_func(self,func, *args):
        """
        @note:跟踪线程返回值，对真正执行的线程函数包一次函数，以获取返回值
        """
        Logger = Trace("benchmark::trace_func")
        try:
            ret,time_consuming = func(*args)        #多线程返回执行结果及执行时间

            self.thread_ret.append(ret)
            self.time_consuming_list.append(time_consuming)
            # if ret != True:
            #     Logger.error('ret = %s '%ret)
            # else:
            #     Logger.info('ret = %s '%ret)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error("error:%s"%errMsg)
            return False

    def runConcurrency(self,func,*params):
        """
        :param comm_params:
        :param private_check_coupons_param:
        :return:
        """
        Logger = Trace("benchmark::runConcurrency")
        try:
            ret = False
            begin_time = time.time()
            ret = func(*params)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error("error: %s" % errMsg)
            ret = False
        finally:
            end_time = time.time()
            time_consuming = end_time - begin_time
            #self.time_consuming_list.append(time_consuming)
            return ret,time_consuming

#
# begin_time = time.time()
# last_line="Transactions:%s,Availability:%s,Elapsed_time:%s,Data_transferred:%s,Response_time:%s,Transaction_rate:%s,Throughput:%s,Concurrency:%s,Successful_transactions:%s,Failed_transactions:%s,Longest_transaction:%s,Shortest_transaction:%s"
# print last_line
# #print 'last_linelen',len(last_line.split(',')),last_line.split(',')
# def write_data(filehandle):
#
#     Concurrency = threading.activeCount()-2
#     haveruntime = time.time() - begin_time
#     try :
#         Availability = ( pass_amount*1.0/total_amount )
#         Response_time = ( total_time/pass_amount )
#         Transaction_rate = ( pass_amount/haveruntime )
#         Throughput = ( downloaded/total_time )/(1024*1024)
#     except Exception, e:
#         print 'write data error%s'%e
#         Availability = 0
#         Response_time = 0
#         Transaction_rate = 0
#         Throughput = 0
#
#     Concurrency = threading.activeCount()-2
#     haveruntime = time.time() - begin_time
#     print 'haveruntime=',haveruntime
#     data= (int(total_amount),#执行次数
#                   round(Availability*100.0,1),#成功率
#                   round(haveruntime,3),#总耗时
#                   round(downloaded/(1048576.0),3 ),#数据量(MB)
#                   round(Response_time*1000,3),#响应时间(ms)
#                   round(Transaction_rate,3),#执行率(t/s)
#                   round(Throughput,2),#吞吐速度(mb/s)
#                   round(Concurrency,3),#并发个数
#                   int(pass_amount),#成功次数
#                   int(total_amount-pass_amount),#失败次数
#                   round(Longest_transaction,2),#最长响应时间
#                   round(Shortest_transaction*1000,2)#最短响应时间
#                       )
#
#     print 'format data =',data
#     result = last_line%data
#
#     tmp=[e.split(":")[1] for e in result.strip().split(",")]
#     print 'tmp=',tmp
#     print time.ctime(),'result =',result
#     filehandle.write(result+'\n')
#     filehandle.flush()
#
#
#
# class Test(threading.Thread):
#     def __init__(self,name):
#         threading.Thread.__init__(self)
#         self.name = 'thread_'+str(name)
#         self.data = StringIO.StringIO()
#         self.curl = pycurl.Curl()
#         self.total_time = 0.0
#         self.downloaded = 0.0
#         self.pass_amount  = 0.0
#         self.total_amount = 0.0
#         self.curl.setopt(pycurl.NOPROGRESS, 1)
#         self.curl.setopt(pycurl.WRITEFUNCTION, self.data.write)
#         self.curl.setopt(pycurl.MAXREDIRS, 5)
#         self.curl.setopt(pycurl.USERAGENT, "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; InfoPath.2)")
#         self.curl.setopt(pycurl.NOSIGNAL, 1)
#         self.info = {
#                      'Transactions':0,
#                      'Availability':0.0,
#                      'Elapsed_time':0,
#                      'Data_transferred':0,
#                      'Response_time':0,
#                      'Transaction_rate':0,
#                      'Throughput':0,
#                      'Concurrency':1,
#                      }
#
#     def run (self):
#         """
#         主程序,对单个url做不断的请求,直到规定时间到,自动结束生命周期
#         """
#         while True:
#             try:
#                 global error_amount,Longest_transaction,Shortest_transaction,pass_amount,total_amount,downloaded,total_time
#
#                 #控制单个线程的生命时间
#
#                 if time.time()-begin_time>run_time:
#                     break
#
#                 url = random.choice(urllist)
#                 print url,'name',self.name
# #                    c = pycurl.Curl()
#                 self.curl.setopt(pycurl.URL, url)
#                 self.curl.perform()
#
#                 self.total_time += self.curl.getinfo(pycurl.TOTAL_TIME)
#                 total_time += self.curl.getinfo(pycurl.TOTAL_TIME)
#                 self.downloaded += self.curl.getinfo(pycurl.SIZE_DOWNLOAD)
#                 downloaded+= self.curl.getinfo(pycurl.SIZE_DOWNLOAD)
#
#                 #获取最小响应时间和最长响应时间,不断的替换这2个全局变量
#                 if self.curl.getinfo(pycurl.TOTAL_TIME) > Longest_transaction:
#                     Longest_transaction = self.curl.getinfo(pycurl.TOTAL_TIME)
#                 if self.curl.getinfo(pycurl.TOTAL_TIME) < Shortest_transaction :
#                     Shortest_transaction = self.curl.getinfo(pycurl.TOTAL_TIME)
#
#                 #计算成功和总执行次数
#                 self.pass_amount += 1
#                 pass_amount =pass_amount + 1
#                 self.total_amount +=1
#                 total_amount =total_amount + 1
#
#                 #计算成功和总执行次数
#
#                 if self.total_time and self.pass_amount:
#                     self.info = {
#                          'Transactions':self.total_amount,
#                          'Concurrency':1,
#                          'Successful_transactions':self.pass_amount,
#                          'Elapsed_time':self.total_time,
#                          'Data_transferred':self.downloaded,
#
#                          'Availability':self.pass_amount/self.total_amount,
#                          'Response_time':self.total_time/self.pass_amount,
#                          'Transaction_rate':self.pass_amount/self.total_time,
#                          'Throughput':self.downloaded/self.total_time
#                          }
#             except Exception, e:
#                 error_amount +=1
#                 self.total_amount +=1
#                 total_amount =total_amount + 1
#                 self.curl = pycurl.Curl()
#                 print "self.curl.perform() Exception : %s"%e
#         self.curl.close()
#     def progress(self,download_t, downloaded, upload_total, uploaded):
# #        print 'progress=',download_t,downloaded,upload_total,uploaded
#         pass
#
#
# class Collector(threading.Thread):
#     """
#     收集每个线程的数据来汇总结果,每6秒往日志文档写一次数据
#     """
#     def __init__(self,path = 'result.log'):
#         threading.Thread.__init__(self)
#         self.log_path = path
#         self.name = 'collector'
#
#     def run (self):
# #        try:
#         log = open(log_path,'a')
#         while True:
# #            global error_amount,Longest_transaction,Shortest_transaction,pass_amount,threads_dict,total_amount,downloaded,total_time
#
#             write_data(log)
#             time.sleep(6)
#             if time.time()-begin_time>run_time+4:
#                 write_data(log)
#                 time.sleep(3)
#                 break
#         write_data(log)
# #        except Exception, e:
# #            print "Collector Exception : %s"%e
#         log.close()
#
# if __name__=='__main__':
#     """
#     获取输入参数
#     """
#     if len(sys.argv)>2 :
#         print 'sys.argv=',sys.argv
#         cmd = str(sys.argv[-4]).replace('~amp;','&')#url地址
#         sleep_time = int(sys.argv[-3])#-time.time()#过几秒后开始执行,这个参数是配合分布式,多台机器一起跑脚本时用到,单个执行不是很重要
#         threads_amount = int(sys.argv[-2])#并发量,创建多少线程
#         log_path=str(sys.argv[-1])  #日志文件地址
#     else:
#         """
#         无输入参数时的默认参数
#         """
#         cmd = '023.baiwandian.cn'
#         sleep_time = 3
#         threads_amount = 800
#         log_path = 'result.log'
#
#     r_file = open(log_path,'a')
#     init = last_line%(0,0,0,0,0,0,0,0,0,0,0,0)
#     r_file.write(init+'\n')
#     r_file.close()
#
#     if sleep_time>0:
#         print 'will sleep %d s'%sleep_time
#         time.sleep(sleep_time)
#         print 'start work~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
#
#     urls = cmd.split('@')
#
#     c = Collector(log_path)
#     collector = [c]
#     c.setDaemon(1)
#     c.start()
#
#     urllist = urls
#     print 'urllist=',urllist
#
#
#     for i in range(threads_amount):
#         t = Test(i)
#         threads_dict[t.name] = t
#
#     print 'threads_dict',threads_dict
#
#     for t in threads_dict.values():
#         t.setDaemon(1)
#         t.start()
#         print t.name,'have started'
#
#     for th in threads_dict.values():
#         th.join()
#         print 'name=',th.name,'info=',th.info
#         print th.name,'have dead'
#
#     for th in collector:
#         th.join()
#         f = open(log_path,'a')
#
#
#     print 'Longest_transaction=',Longest_transaction,
#     print 'Shortest_transaction=',Shortest_transaction,
#     print 'error_amount=',error_amount
#     print 'pass_amount=',pass_amount
#     print 'total_amount=',total_amount
#     print 'Availability=',(pass_amount/total_amount)*100.0
#     print 'total_time=',total_time
#
#
#     print 'over'