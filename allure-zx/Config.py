#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
Created on June 12, 2019
@author: hzhuangfg
配置信息
'''


def get_base_url(env):
    if env == 'test':
        base_url = 'http://114.116.163.85:9997'  # 测试地址
    elif env == 'preview':
        base_url = 'http://preview.hoolink.com'  # 预览地址
    elif env == 'online':
        base_url = 'http://cloud.hoolink.com'  # 正式地址
    elif env == 'smoke':
        base_url = 'http://192.168.1.163:9997'  # 冒烟环境
    elif env == 'pme':
        base_url = 'http://117.78.51.74:9997'  # 压测环境
    elif env == 'mockPme':
        base_url = 'http://49.4.49.173:8998'  # mockPme服务
    else:
        base_url = 'http://192.168.1.189'
    return base_url


def get_manage_url(env):
    if env == 'test':
        base_url = 'http://114.116.163.85:9101'  # 测试地址
    elif env == 'preview':
        base_url = 'http://preview.hoolink.com'  # 预览地址
    elif env == 'online':
        base_url = 'http://cloud.hoolink.com'  # 正式地址
    elif env == 'smoke':
        base_url = 'http://192.168.1.163:9997'  # 冒烟环境
    elif env == 'pme':
        base_url = 'http://117.78.51.74:9997'  # 压测环境
    elif env == 'mockPme':
        base_url = 'http://49.4.49.173:8998'  # mockPme服务
    else:
        base_url = 'http://192.168.1.189'
    return base_url


mock_server_ip = "192.168.1.18"
mock_server_port = 5000

dbhost = "10.100.98.91"
dbport = "3306"
# 测试数据库的信息
dbhost = "114.116.65.155"
dbport = 8635
dbuser = "admin"
dbpass = "Hoolink#testrds2019"
# common paramters
log_ip = '125.120.84.72'
user_agent = 'mozilla/4.0 (compatible; msie 6.0; windows nt 5.1;sv1)'
whether_send_mail = False  # 失败是否发邮件

# Log config
LOG_MAX_SIZE = 10 * 1024 * 1024  # 单个日志文件最大10M
LOG_MAX_FILES = 1000  # 1000 Files:log.1,log.2,log.3,log.4 ....

pwd_need_md5 = True
concurrence_fail_rate = 5
