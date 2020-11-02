#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on June 26, 2019
@author: hzhuangfg
 基础库
'''
import os
import sys
import time
import glob
import httplib,urllib,urllib2
import requests
import re
import random
import binascii
import smtplib
from email.mime.text import MIMEText
import traceback
from com.mysql import *
import Config
from fs.Trace import Trace
from com.json_processor import JSONProcessor
import redis
import datetime
import json
import sys
reload(sys)
global prjDir
sys.setdefaultencoding('utf-8') #修改默认的编码模式

prjDir = os.path.split(os.path.realpath(__file__))[0]
prjDir=os.path.join(prjDir, '..//')
configfile_path = os.path.join(prjDir, "config.ini")

def to_bool(strVar):
    """
    字符串转bool
    :param strVar:
    :return:
    """
    Logger = Trace("Lib::to_bool")
    try:
        strIn=str(strVar)
        strBool=strIn.lower()
        strBool=strBool.strip()
        false_dict={'False':False,'false':False, 'none':False}
        ret=false_dict.get(strBool, True)
        return ret
    except Exception, e:
        Logger.critical("Exception", e)
        return False
