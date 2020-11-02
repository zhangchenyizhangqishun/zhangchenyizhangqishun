#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on June 20, 2019
@author: hzhuangfg
基础库
'''
import csv
import datetime
import random
from Config import *
from fs.Trace import Trace
import hashlib
import traceback
import shlex
import os
import base64
import urllib
import io
import socket,struct
from selenium.webdriver.common.by import By
from com.human_time import *
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式

def generate_time(action,day):
    nowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    retTime = None
    if action == 'sub_day':
        retTime = HumanDateTime(nowTime).sub_day(day).strftime('%Y-%m-%d %H:%M:%S')
    elif action == 'add_day':
        retTime = HumanDateTime(nowTime).sub_day(day).strftime('%Y-%m-%d %H:%M:%S')
    return retTime

def get_pwd_need_md5(str):
    """
    登录密码MD5加密：用户在登录密码时，前端进行MD5加密，初始密码123456不进行加密
    加密场景包括登录、首次修改、个人中心修改密码
    加密规则：非123456密码输入完成之后，字符串前面拼接e+iot，进行两次MD5加密，然后传递给后端，如果重置密码还是123456，前端直接判断不允许重置123456。
    例子：输入了654321，是对e+iot654321进行两次MD5加密
    :param str:
    :return:
    """
    Logger = Trace("Lib::get_pwd_need_md5")
    try:
        # if pwd_need_md5 and str != '123456':
        if pwd_need_md5:
            str = 'e+iot' + str
            return gen_md5_sign((gen_md5_sign(str)))
        return str
    except Exception, e:
        errMsg = traceback.format_exc()
        Logger.error("error: %s" % errMsg)
        return None


def get_cloud_pwd_need_md5(str):
    """
    登录密码MD5加密：用户在登录密码时，前端进行MD5加密，初始密码123456不进行加密
    加密场景包括登录、首次修改、个人中心修改密码
    加密规则：非123456密码输入完成之后，字符串前面拼接e+iot，进行两次MD5加密，然后传递给后端，如果重置密码还是123456，前端直接判断不允许重置123456。
    例子：输入了654321，是对e+iot654321进行两次MD5加密
    :param str:
    :return:
    """
    Logger = Trace("Lib::get_pwd_need_md5")
    try:
        # if pwd_need_md5 and str != '123456':
        if pwd_need_md5:
            # str = 'e+iot' + str
            return gen_md5_sign(str)
        return str
    except Exception, e:
        errMsg = traceback.format_exc()
        Logger.error("error: %s" % errMsg)
        return None

def year():
    '''生成年份'''
    now = time.strftime('%Y')
    #1948为第一代身份证执行年份,now-18直接过滤掉小于18岁出生的年份
    second = random.randint(1948,int(now)-18)
    age = int(now) - second
    print('随机生成的身份证人员年龄为：'+str(age))
    return second


def month():
    '''生成月份'''
    three = random.randint(1,12)
    #月份小于10以下，前面加上0填充
    if three < 10:
        three = '0' + str(three)
        return three
    else:
        return three


def day():
    '''生成日期'''
    four = random.randint(1,31)
    #日期小于10以下，前面加上0填充
    if four < 10:
        four = '0' + str(four)
        return four
    else:
        return four


def randoms():
    '''生成身份证后四位'''
    #后面序号低于相应位数，前面加上0填充
    five = random.randint(1,9999)
    if five < 10:
        five = '000' + str(five)
        return five
    elif 10 < five < 100:
        five = '00' + str(five)
        return five
    elif 100 < five < 1000:
        five = '0' + str(five)
        return five
    else:
        return five


def gen_random_target(target='default'):
    if target == 'mobile':
        random_Target = random.choice(['139','188','185','136','135','158','151'])+"".join(random.choice("0123456789") for _ in range(8))
    elif target == 'password':
        random_Target = random.choice(['fuxiuxia','hfg','hjy'])+"_" + "".join(random.choice("0123456789") for _ in range(8))
    elif target == 'email':
        random_Target = random.choice(['sam','ice','trancy'])+"".join(random.choice("0123456789") for _ in range(8))+"".join('.hoolink.com')
    elif target == 'Lon':
        random_Target = random.choice(['90', '91', '92', '100', '101', '102', '110','111']) + "."+"".join(
            random.choice("0123456789") for _ in range(6))
    elif target == 'Lat':
        random_Target = random.choice(['23', '25', '26', '31', '35', '36', '40','49']) + "."+"".join(
            random.choice("0123456789") for _ in range(6))
    elif target == 'ip':
        RANDOM_IP_POOL = ['192.168.1.222/0']
        str_ip = RANDOM_IP_POOL[random.randint(0, len(RANDOM_IP_POOL) - 1)]
        str_ip_addr = str_ip.split('/')[0]
        str_ip_mask = str_ip.split('/')[1]
        ip_addr = struct.unpack('>I', socket.inet_aton(str_ip_addr))[0]
        mask = 0x0
        for i in range(31, 31 - int(str_ip_mask), -1):
            mask = mask | (1 << i)
        ip_addr_min = ip_addr & (mask & 0xffffffff)
        ip_addr_max = ip_addr | (~mask & 0xffffffff)
        random_Target = socket.inet_ntoa(struct.pack('>I', random.randint(ip_addr_min, ip_addr_max)))
    elif target == 'external':
        random_Target = random.choice(['123', '321', '456', '323', '987', '856', '756']) +"".join(random.choice("0123456789") for _ in range(6))
    elif target == 'port':
        random_Target = random.choice(['12', '32', '45', '32', '97', '85', '76']) +"".join(random.choice("0123456789") for _ in range(2))
    elif target == 'letter':
        random_Target = "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(11))
    elif target == 'plate':
        random_Target = random.choice(['浙', '宁', '川', '甘', '青', '湘', '豫']) + random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G']) + "".join(
            random.choice("0123456789") for _ in range(5))
    elif target == 'cardId':
        first = regiun()
        second = year()
        three = month()
        four = day()
        last = randoms()
        random_Target = str(first)+str(second)+str(three)+str(four)+str(last)
    else:
        random_Target ="".join(random.choice("1234567890") for _ in range(11))
    return random_Target


def load_csv_file(csv_file):
    """
    获取csv文件有效参数字段对应的值，以列表形式返回，case描述字段单独以列表返回
    (
        [
            [u'admin', u'888888', u'17', u'[6,9]', u'登录成功'],
            [u'admin', u'888888', u'18', u'[9,]', u'用户更新成功']
        ],
        [u'登录成功,测试', u'用户更新成功,你好']
    )
    """
    csv_data_list = []
    csv_desc_list = []
    keys = []
    """
    获取csv文件有效参数字段->有序
    ['account', 'passWord', 'roleId', 'projectIds', 'expectedMessage']
    """
    with io.open(csv_file, encoding='utf-8') as data_file:
        for line in data_file:
            line = line.replace('\n', '')
            str = shlex.shlex(line.encode('unicode-escape'), posix=True)
            str.whitespace = ','
            str.whitesapce_split = True
            # str.quotes = ''
            line_data = list(str)
            if line_data == [""]:           #忽略空行
                continue
            for index, parameter_name in enumerate(line_data):
                if parameter_name.lower() != 'caseid' and parameter_name.lower() != 'desc' \
                        and parameter_name.lower()!= 'index' and parameter_name.lower() != 'dbcheckpath' \
                        and parameter_name.lower() != 'dbcheckindex' and parameter_name.lower() != 'comment'\
                        and parameter_name.lower() != 'isrun':
                    keys.append(parameter_name)
            break

    with io.open(csv_file, encoding='utf-8') as data_file:
        reader = csv.DictReader(data_file)
        for line in reader:
            line_data = line
            data = []
            """
            {
                'account': 'admin', 'roleId': '17', 'isRun': 'True', 'caseId': '1001', 
                'expectedMessage': '登录成功','projectIds': '[6,9]', 'passWord': '888888', 
                'desc': '登录成功,测试'
             }
            """
            for key in keys:
                for parameter_key,parameter_name in line_data.iteritems():
                    if line_data['isRun'].lower() == 'true':
                        if key == parameter_key:
                            if parameter_key.lower() == 'expectedmessage':
                                if parameter_name.lower() == 'none':        # [hoolink-rpc.web.UserController.createUser]. Parameter is [createUser]. Processor is [body].
                                    parameter_name = eval(parameter_name)   # 'None' --> None
                                data.append(parameter_name)
                            elif parameter_name.lower() == 'true' or parameter_name.lower() == 'false' or parameter_name.lower() == 'none':
                                parameter_name = eval(parameter_name)       #'True' --> True,'None' --> None,
                                data.append(parameter_name)
                            elif (parameter_name.find('[') != -1 and parameter_name.find(']') != -1):   #'[1,2,3]' --> [1,2,3],"['鸣志智能照明设备','互灵NB智能照明设备']" --> ['鸣志智能照明设备','互灵NB智能照明设备']
                                # parameter_name = parameter_name.decode('utf-8')
                                parameter_name = eval(parameter_name)
                                data.append(parameter_name)
                            else:
                                data.append(parameter_name.decode('utf-8'))
            #单独以列表形式返回case描述字段
            for parameter_key, parameter_name in line_data.iteritems():
                if line_data['isRun'].lower() == 'true':
                    if parameter_key.lower() == 'desc':
                        # print 'parameter_name = %s' % parameter_name.decode('utf-8')
                        csv_desc_list.append(parameter_name.decode('utf-8'))
            if data:
                csv_data_list.append(data)
    return csv_data_list, csv_desc_list