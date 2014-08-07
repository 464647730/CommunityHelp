__all__=["Push"]

from igt_push import *
from igetui.template import *
from igetui.template.igt_base_template import *
from igetui.template.igt_transmission_template import *
from igetui.template.igt_link_template import *
from igetui.template.igt_notification_template import *
from igetui.template.igt_notypopload_template import *
from igetui.igt_message import *
from igetui.igt_target import *
from igetui.template import *

class Push:

    __APPKEY = "r3Gm2zkRsb8QLMq2U92Bi8"
    __APPID = "0yZq9kruSq8zvSpYB2UiA1"
    __MASTERSECRET = "h8Ppk4heNR6MACNWjN3XB2"
    __HOST = 'http://sdk.open.api.igexin.com/apiex.htm'


    __TEMPLATE = TransmissionTemplate()

    def __init__(self):

        self.__TEMPLATE = TransmissionTemplate()
        self.__TEMPLATE.transmissionType = 2
        self.__TEMPLATE.appId = self.__APPID
        self.__TEMPLATE.appKey = self.__APPKEY

    def pushToSingle(self, CID, content):
        push = IGeTui(self.__HOST, self.__APPKEY, self.__MASTERSECRET)

        self.__TEMPLATE.transmissionContent = content

        message = IGtSingleMessage()
        message.isOffline = True
        message.offlineExpireTime = 1000 * 3600 * 12
        message.data = self.__TEMPLATE

        target = Target()
        target.appId = self.__APPID
        target.clientId = CID

        ret = push.pushMessageToSingle(message, target)
        return ret

    def pushToList(self, CIDList, content, details=False):
        push = IGeTui(self.__HOST, self.__APPKEY, self.__MASTERSECRET)

        self.__TEMPLATE.transmissionContent = content

        os.environ['needDetails'] = 'true' if details else 'false'

        message = IGtListMessage()
        message.data = self.__TEMPLATE
        message.isOffline = True
        message.offlineExpireTime = 1000 * 3600 * 12

        targets = [];

        for index in range(len(CIDList)):
            target = Target()
            target.appId = self.__APPID
            target.clientId = CIDList[index]
            targets.append(target)

        contentId = push.getContentId(message)
        ret = push.pushMessageToList(contentId, targets)
        return ret

    def pushToAll(self, content):
        push = IGeTui(self.__HOST, self.__APPKEY, self.__MASTERSECRET)

        self.__TEMPLATE.transmissionContent = content

        message = IGtAppMessage()
        message.data = self.__TEMPLATE
        message.isOffline = True
        message.offlineExpireTime = 1000 * 3600 * 12
        message.appIdList.extend([self.__APPID])

        ret = push.pushMessageToApp(message)
        return ret

    def getUserStatus(self, CID):
        push = IGeTui(self.__HOST, self.__APPKEY, self.__MASTERSECRET)
        return push.getClientIdStatus(self.__APPID, CID)

    def stopTask(self):
        push = IGeTui(self.__HOST, self.__APPKEY, self.__MASTERSECRET)
        return push.stop("OSA-0226_50RYYPFmos9eQEHZrkAf27")
