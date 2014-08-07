# -*- coding: utf-8 -*-
__author__ = 'wei'

import hashlib
import time
import urllib, urllib2, json
import base64
import os


class IGeTui:
    def __init__(self, host, appKey, masterSecret):
        self.host = host
        self.appKey = appKey
        self.masterSecret = masterSecret

    def connect(self):
        timenow = self.getCurrentTime()
        sign = self.getSign(self.appKey, timenow, self.masterSecret)
        params = {}
        params['action'] = 'connect'
        params['appkey'] = self.appKey
        params['timeStamp'] = timenow
        params['sign'] = sign

        rep = self.httpPost(params)

        if 'success' == (rep['result']):
            return True

        print rep
        raise Exception(str(rep) + "appKey or masterSecret is auth failed.")
        return False

    def pushMessageToSingle(self, message, target):
        params = {}
        params['action'] = "pushMessageToSingleAction"
        params['appkey'] = self.appKey
        transparent = message.data.getTransparent()
        params['clientData'] = base64.encodestring(transparent.SerializeToString())
        params['transmissionContent'] = message.data.transmissionContent
        params['isOffline'] = message.isOffline
        params['offlineExpireTime'] = message.offlineExpireTime
        params['appId'] = target.appId
        params['clientId'] = target.clientId
        params['type'] = 2 #default is message
        params['pushType'] = message.data.pushType
        return self.httpPostJson(params)

    def pushMessageToApp(self, message):
        params = {}
        params['action'] = "pushMessageToAppAction"
        params['appkey'] = self.appKey

        transparent = message.data.getTransparent()
        params['clientData'] = base64.encodestring(transparent.SerializeToString())
        params['transmissionContent'] = message.data.transmissionContent
        params['isOffline'] = message.isOffline
        params['offlineExpireTime'] = message.offlineExpireTime
        params['appIdList'] = message.appIdList
        params['phoneTypeList'] = message.phoneTypeList
        params['provinceList'] = message.provinceList
        params['type'] = 2 # default is message
        params['pushType'] = message.data.pushType
        params['tagList'] = message.tagList

        return self.httpPostJson(params)

    def pushMessageToList(self, contentId, targets):
        params = {}
        params['action'] = 'pushMessageToListAction'
        params['appkey'] = self.appKey
        params['contentId'] = contentId
        needDetails = os.getenv("needDetails","false")
        params['needDetails'] = needDetails
        targetList = []
        for target in targets:
            appId = target.appId
            clientId = target.clientId
            target = {"appId": appId, "clientId": clientId}
            targetList.append(target)

        params['targetList'] = targetList
        params['type'] = 2
        return self.httpPostJson(params)

    def stop(self, contentId):
        params = {}
        params['action'] = 'stopTaskAction'
        params['appkey'] = self.appKey
        params['contentId'] = contentId

        ret = self.httpPostJson(params)
        if ret["result"]=='ok':
            return True
        return False

    def getClientIdStatus(self, appId, clientId):
        params = {}
        params['action'] = 'getClientIdStatusAction'
        params['appkey'] = self.appKey
        params['appId'] = appId
        params['clientId'] = clientId

        return self.httpPostJson(params)

    def getContentId(self, message):
        params = {}
        params['action'] = "getContentIdAction"
        params['appkey'] = self.appKey
        transparent = message.data.getTransparent()
        params['clientData'] = base64.encodestring(transparent.SerializeToString())
        params['transmissionContent'] = message.data.transmissionContent
        params["isOffline"] = message.isOffline
        params["offlineExpireTime"] = message.offlineExpireTime
        params["pushType"] = message.data.pushType
        ret = self.httpPostJson(params)

        return ret['contentId'] if ret['result'] == 'ok' else ' '

    def cancelContentId(self, contentId):
        params = {}
        params['action'] = 'cancleContentIdAction'
        params['contentId'] = contentId
        ret = self.httpPostJson()
        return True if ret['result'] == 'ok' else False

    def getCurrentTime(self):
        return (int)(time.time() * 1000)

    def getSign(self, appKey, timeStamp, masterSecret):
        rawValue = appKey + str(timeStamp) + masterSecret
        return hashlib.md5(rawValue.encode()).hexdigest()

    def httpPostJson(self, params):
        params['version'] = '3.0.0.0'
        ret = self.httpPost(params)
        if ret is not None and "sign_error" == ret["result"]:
            self.connect()
            ret = self.httpPost(params)
        return ret

    def httpPost(self, params):
        #如果通过代理访问我们接口，需要自行配置代理，示例如下：
        #opener = urllib2.build_opener(urllib2.ProxyHandler({'http':'192.168.1.108:808'}), urllib2.HTTPHandler(debuglevel=1))
        #urllib2.install_opener(opener)
        data_json = json.dumps(params)
        req = urllib2.Request(self.host, data_json)
        retry_time_limit = 3
        isFail = True
        tryTime = 0
        while isFail and tryTime < retry_time_limit:
            try:
                res_stream = urllib2.urlopen(req, timeout=60)
                isFail = False
            except:
                isFail = True
                tryTime += 1
                print("try " + str(tryTime) + " time failed, time out.")

        page_str = res_stream.read()
        page_dict = eval(page_str)
        return page_dict
