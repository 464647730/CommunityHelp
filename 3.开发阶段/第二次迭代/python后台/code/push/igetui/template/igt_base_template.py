#coding: utf-8

from push.protobuf import *
import json


class BaseTemplate:
    def __init__(self):
        self.appKey = ""
        self.appId = ""
        self.pushInfo = None

    def getTransparent(self):
        transparent = gt_req_pb2.Transparent()
        transparent.id = ""
        transparent.action = "pushmessage"
        transparent.taskId = ""
        transparent.appKey = self.appKey
        transparent.appId = self.appId
        transparent.messageId = ""
        transparent.pushInfo.CopyFrom(self.getPushInfo())
        actionChains = self.getActionChains()
        for actionChain in actionChains:
            tmp = transparent.actionChain.add()
            tmp.CopyFrom(actionChain)
        return transparent

    def getActionChains(self):
        return []

    def getPushInfo(self):
        if self.pushInfo is None:
            self.pushInfo = gt_req_pb2.PushInfo()
            self.pushInfo.message = ""
            self.pushInfo.actionKey = ""
            self.pushInfo.sound = ""
            self.pushInfo.badge = ""
        return self.pushInfo

    def setPushInfo(self, actionLocKey, badge, message, sound, payload, locKey, locArgs, launchImage):
        self.pushInfo = gt_req_pb2.PushInfo()
        self.pushInfo.actionLocKey = actionLocKey
        self.pushInfo.badge = str(badge)
        self.pushInfo.message = message.decode("utf-8")
        self.pushInfo.sound = sound
        self.pushInfo.payload = payload
        self.pushInfo.locKey = locKey
        self.pushInfo.locArgs = locArgs
        self.pushInfo.launchImage = launchImage

        isValidate = self.validatePayload(locKey, locArgs, message, actionLocKey, launchImage, str(badge), sound, payload)
        if isValidate is False:
            payloadLen = self.validatePayloadLength(locKey, locArgs, message, actionLocKey, launchImage, str(badge), sound, payload)
            raise Exception("PushInfo length over limit: " + str(payloadLen) + ". Allowed: 256.")


    def processPayload(self, locKey, locArgs, message, actionLocKey, launchImage, badge, sound, payload):
        map = {}
        apnsMap = {}
        alertMap = {}

        if sound is not None and len(sound) > 0:
            apnsMap["sound"] = sound
        else:
            apnsMap["sound"] = "default"
        if launchImage is not None and len(launchImage) > 0:
            alertMap["launch-image"] = launchImage
        if locKey is not None and len(locKey) > 0:
            alertMap["loc-key"] = locKey
            if locArgs is not None and len(locArgs) > 0:
                alertMap["loc-args"] = locArgs.split(",")
        elif message is not None and len(message) > 0:
            alertMap["body"] = message

        if actionLocKey is not None and len(actionLocKey) > 0:
            alertMap["action-loc-key"] = actionLocKey

        apnsMap["badge"] = self.toInt(badge, 0)

        if payload is not None and len(payload) > 0:
            map["payload"] = payload

        map["aps"] = apnsMap
        apnsMap["alert"] = alertMap
        return map

    def validatePayload(self, locKey, locArgs, message, actionLocKey, launchImage, badge, sound, payload):
        map = self.processPayload(locKey, locArgs, message, actionLocKey, launchImage, badge, sound, payload)
        jsonData = json.dumps(map, separators=(',', ':'), ensure_ascii=False)
        if len(jsonData)>256:
            return False
        return True

    def validatePayloadLength(self, locKey, locArgs, message, actionLocKey, launchImage, badge, sound, payload):
        map = self.processPayload(locKey, locArgs, message, actionLocKey, launchImage, badge, sound, payload)
        jsonData = json.dumps(map, separators=(',', ':'), ensure_ascii=False)
        return len(jsonData)

    def toInt(self, strr, defaultValue):
        if strr is None or strr == "":
            return defaultValue
        return int(strr)

