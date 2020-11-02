#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on July 12, 2019
@author: hzhuangfg
'''
from business.ability import *
from check.checkHoolinkAbility import CheckResult
from com.api import logging
from com.util import gen_md5_sign
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #修改默认的编码模式

class abilityTool():
    def __init__(self,logId,env='test',http_client=None):
        self.env = env
        self.logId = gen_md5_sign(logId)
        self.projectId = 'hoolink'
        self.ability = ability(self.logId,self.env,http_client)
        self.checker = CheckResult(self.logId,self.env,http_client)
        self.http_client = http_client            #locust client or requests cient
        self.logger = Trace('abilityTool')

    @logging("abilityTool", "uploadCustom")
    def uploadCustom(self,filePath,token):
        """
        上传模型文件
        """
        resp = self.ability.uploadCustom(filePath,token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("abilityTool", "uploadFile")
    def uploadFile(self,filePath,token):
        """
        上传图片
        """
        resp = self.ability.uploadFile(filePath,token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("abilityTool", "readFileById")
    def readFileById(self,fileId,token):
        """
        读取上传文件
        """
        resp = self.ability.readFileById(fileId,token).json
        resp['checker'] = self.checker.check_readFileById(resp)
        return resp

    @logging("abilityTool", "uploadSampleFace")
    def uploadSampleFace(self,projectId,filePath,token):
        """
        上传样本图片
        """
        resp = self.ability.uploadSampleFace(projectId,filePath,token)
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("abilityTool", "searchFaceBySampleFace")
    def searchFaceBySampleFace(self,projectId,maxResult,similarity,faceContrastTargets,token):
        """
        人脸检索
        """
        resp = self.ability.searchFaceBySampleFace(projectId,maxResult,similarity,faceContrastTargets,token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("abilityTool", "uploadFaceToObs")
    def uploadFaceToObs(self,projectId,filePath,token):
        """
        上传人脸图片到obs
        """
        resp = self.ability.uploadFaceToObs(projectId,filePath,token)
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("abilityTool", "createFaceLabel")
    def createFaceLabel(self,bucketName,objectKey,faceSetName,token):
        """
        创建人脸标签
        """
        resp = self.ability.createFaceLabel(bucketName,objectKey,faceSetName,token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("abilityTool", "getAloneCameraLiveStream")
    def getAloneCameraLiveStream(self,projectId,cameraId,token):
        """
        查询独立子设备视频转码
        """
        resp = self.ability.getAloneCameraLiveStream(projectId,cameraId,token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    @logging("abilityTool", "start")
    def start(self,cameraId,channelNo,deviceSerial,ptzCommand,speed,token):
        """
        云台控制
        """
        resp = self.ability.start(cameraId,channelNo,deviceSerial,ptzCommand,speed,token).json
        resp['checker'] = self.__dealwithCommResp__(resp)
        return resp

    def __dealwithCommResp__(self,resp):
        """
        :param resp:
        :return:
        """
        Logger = Trace("tool::__dealwithCommResp__")
        try:
            if resp is not None and  resp.has_key('data'):
                if resp.status is True:
                    return True
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False


    def __dealwithLocustResp__(self,resp):
        """
        :param resp:
        :return:
        """
        Logger = Trace("tool::__dealwithLocustResp__")
        try:
            # Logger.debug(self.logId,'body = %s'%(json.dumps(resp,ensure_ascii=False,indent=4).decode('utf8')))
            if resp is not None:
                if resp.status is True and self.http_client is not None:
                    return True
            return False
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId,"error: %s" % errMsg)
            return False
