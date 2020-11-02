#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
Created on June 14, 2019
@author: hzhuangfg
'''
from com.Lib import *
from engine.runner import Runner
from com.api import request,logging
from Config import get_manage_url
from datetime import datetime
from com.human_time import HumanDateTime
class ability(object):

    def __init__(self, logId, env='test', http_client=None):
        self.appid = self.logId = logId
        self.base_url = get_manage_url(env)
        self.http_client = http_client
        self.runner = Runner(http_client)
        self.common_params = {"http_client_session": self.http_client}

    @logging("ability", "uploadCustom")
    @request(url='/api/hoolink-ability/web/obs/uploadCustom', method='post',headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'})
    def uploadCustom(self,filePath,token):
        """
        上传模型文件
        """
        files = {'file': open(filePath, 'rb')}
        params = {'files':files,"X-Token": token}
        return dict(params, **self.common_params)

    @logging("ability", "edmClaimUploadId")
    @request(url='/api/hoolink-ability/web/combine/edmClaimUploadId', method='post',headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'})
    def edmClaimUploadId(self,fileName,token):
        """
        上传图片
        """
        # files = {'partFile': open(filePath, 'rb')}
        params = {'data':fileName,"X-Token": token}
        # return dict(params, **self.common_params)
        return self.__joinParamKey__(params)
    @logging("ability", "edmClaimUploadId")
    @request(url='api/hoolink-ability/web/obs/edmClaimUploadId', method='post',headers={"Content-Type":"application/json"})
    def readFileById(self,fileName,token):
        """
        获取文件分片上传uploadId
        """
        params = {'data': fileName, "X-Token": token}
        return self.__joinParamKey__(params)

    # @request(url='/api/hoolink-ability/web/combine/edmUploadPart', method='post', headers={'Content-Type': 'multipart/form-data;boundary=----WebKitFormBoundaryhhcGyz8lrzbVCeXf'})
    def edmUploadPart(self, filePath,fileName,fileSize,partNum,uploadIdAndAliasPairList, token):
        """
        文件分块上传
        """
        Logger = Trace("ability::edmUploadPart")
        try:

            combineUploadPartParamStr = {'uploadIdAndAliasPairList':uploadIdAndAliasPairList,'fileName':fileName,'fileSize':fileSize,'partNum':partNum}
            files = {'file':open(filePath,'rb')}
            params = {'combineUploadPartParamStr':combineUploadPartParamStr,'id':'WU_FILE_6','fileName':'888.jpg','type':'image/jpeg','size':'57023','lastModifiedDate':'Thu Feb 21 2019 16:33:53 GMT 0800 (中国标准时间)'}
            headers = {'Content-Type': 'multipart/form-data',"X-Token": token}
            data_result = requests.post(self.base_url + '/api/hoolink-ability/web/combine/edmUploadPart',params,files=files, headers=headers)
            resp = data_result.json()
            return JSONProcessor(resp)
        except Exception, e:
            errMsg = traceback.format_exc()
            Logger.error(self.logId, "error: %s" % errMsg)
            return None

    @logging("ability", "uploadSampleFace")
    def uploadSampleFace(self,projectId, filePath, token):
        """
        上传样本图片
        """
        files = {'faceimg': open(filePath, 'rb')}
        headers = {"X-Token": token}
        data_param = {'projectId': projectId}
        data_result = requests.post(self.base_url+'/api/ability/webapp/hk/uploadSampleFace', data=data_param, files=files,headers=headers)
        # Logger.info('data_result = %s'%data_result.json())
        resp = data_result.json()
        return JSONProcessor(resp)

    @logging("ability", "searchFaceBySampleFace")
    @request(url='/api/ability/webapp/hk/searchFaceBySampleFace', method='post',headers={"Content-Type":"application/json"})
    def searchFaceBySampleFace(self,projectId,maxResult,similarity,faceContrastTargets,token):
        """
        人脸检索
        """
        nowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        deadTime = HumanDateTime(nowTime).add_day(7).strftime('%Y-%m-%d %H:%M:%S')
        tmp_time = nowTime.split(' ')
        startTime = tmp_time[0] + 'T' + tmp_time[1] + 'Z'
        tmp_time = deadTime.split(' ')
        endTime = tmp_time[0] + 'T' + tmp_time[1] + 'Z'
        targetsList = faceContrastTargets
        data = {'endTime': endTime, "startTime": startTime,'maxResult':maxResult,'projectId':projectId,'similarity':similarity,'targetsList':targetsList}
        params = {'data': data, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("ability", "uploadFaceToObs")
    def uploadFaceToObs(self,projectId,filePath,token):
        """
        上传人脸图片到obs
        """
        files = {'faceFile': open(filePath, 'rb')}
        headers = {"X-Token": token}
        data_param = {'projectId': projectId}
        data_result = requests.post(self.base_url + '/api/ability/webapp/obs/uploadFaceToObs', data=data_param,
                                    files=files, headers=headers)
        resp = data_result.json()
        return JSONProcessor(resp)

    @logging("ability", "createFaceLabel")
    @request(url='/api/ability/webapp/face/createFaceLabel', method='post',headers={"Content-Type":"application/json"})
    def createFaceLabel(self,bucketName,objectKey,faceSetName,token):
        """
        创建人脸标签
        """
        data = {'bucketName':bucketName,'objectKey':objectKey,'faceSetName':faceSetName}
        params = {'data':data,"X-Token": token}
        return self.__joinParamKey__(params)

    @logging("ability", "getAloneCameraLiveStream")
    @request(url='/api/ability/webapp/hls/getAloneCameraLiveStream', method='post',
             headers={"Content-Type": "application/json"})
    def getAloneCameraLiveStream(self,projectId,cameraId,token):
        """
        查询独立子设备视频转码
        """
        params = {'data': {'projectId': projectId, 'cameraId': cameraId}, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("ability", "start")
    @request(url='/api/ability/webapp/hls/ptz/start', method='post',
             headers={"Content-Type": "application/json"})
    def start(self, cameraId,channelNo,deviceSerial,ptzCommand,speed,token):
        """
        云台控制
        """
        params = {'data': {'channelNo': channelNo, 'cameraId': cameraId, 'speed': speed, 'deviceSerial': deviceSerial,
                           'ptzCommand': ptzCommand}, "X-Token": token}
        return self.__joinParamKey__(params)

    @logging("ability", "__joinParamKey__")
    def __joinParamKey__(self, params,method = 'post',**kwargs):
        params = dict({'params': params}, **kwargs) if method is 'GET' else {'data': params}
        return dict(params, **self.common_params)
