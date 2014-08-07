# -*- coding: utf-8 -*-
#数据将在30分钟之后提供查询
#最后更新时间为2013.10.22
import hashlib
import urllib, urllib2, json
def getPushResult(url,appKey,masterSecret,taskId):
    params = {}
    params["action"] = "getPushMsgResult"
    params["appkey"] = appKey
    params["taskId"] = taskId
    sign = createSign(params,masterSecret)
    params["sign"] = sign
    rep = httpPost(url,params)
    return rep
def createSign(params,masterSecret):
    sign = masterSecret
    for (k,v) in params.items():
        sign = sign+k+v
    return hashlib.md5(sign).hexdigest()
def httpPost(url, params):
    data_json = json.dumps(params)
    req = urllib2.Request(url, data_json)
    res_stream = urllib2.urlopen(req, timeout = 60)
    page_str = res_stream.read()
    page_dict = eval(page_str)
    return page_dict
rep = getPushResult("http://sdk.open.api.igexin.com/api.htm","tpDVam96sY8pxhwBupJ462","TBokfpttQJ6aHIhBE9y867","GT_1017_gJs4GvJxZV77gdgBKsuvO9")
print rep
    
    
    
