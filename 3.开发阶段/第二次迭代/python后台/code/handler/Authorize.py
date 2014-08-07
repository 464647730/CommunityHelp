# encoding: utf-8
__author__ = 'Administrator'

import tornado.web
import json
import random
import smtplib
from email.mime.text import MIMEText
from CHRequestHandler import CHRequestHandler, LackParamsException, NoUserException
#
# errorcode:
#   1: 缺少参数
#   2: 用户名错误，用户不存在
#
# 查询用户的认证状态
#
class AuthStateHandler(tornado.web.RequestHandler):
    def post(self):
        print("mark 2")
        content = self.request.body
        j = json.loads(content)
        if j.has_key("username"):
            username = j["username"]
        else:
            error = {
                "error": "lack params",
                "request": "querauthstate",
                "error_code": 1
            }
            self.write(json.dumps(error))
            print("no username supplied")
            return
        user_record = self.application.dbapi.getUserByUserName(username)
        if user_record is None:
            error = {
                "error": "no such user",
                "request": "queryauthstate",
                "error_code": 2
            }
            self.write(json.dumps(error))
            print("no such user")
            return
        uid = user_record["id"]
        auth_record = self.application.dbapi.getAuth(uid)
        if auth_record is None:
            self.application.dbapi.insertAuth(uid)
            auth_record = self.application.dbapi.getAuth(uid)
        result = {
            "email": auth_record["email"],
            "email_state": auth_record["email_state"],
            "phone": auth_record["phone"],
            "phone_state": auth_record["phone_state"]
        }
        print("mark 1")
        resultstr = json.dumps(result)
        print(resultstr)
        self.write(resultstr)



#
# params:
#     username
#     email
# error_code:
#   prefix: 10000
class RequestEmailAuthHandler(tornado.web.RequestHandler):
    codechars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW0123456789"

    host = "114.215.133.61:8080"
    mail_host = "smtp.163.com"
    mail_user = "CommunityHelp"
    mail_pass = "community"
    mail_postfix = "163.com"
    me = mail_user + "<" + mail_user + "@" + mail_postfix + ">"
    msg_content_template = u"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset='utf-8'/>
        </head>
        <body>
            <h1>社区居民求助系统邮箱验证</h1>
            <p>您好！</p>
            <p>您已经成功发出了邮箱验证请求。</p>
            <p>点击以下链接即可完成邮箱验证。如果无法点击，请手动复制网址到浏览器打开。</p>
            <p><a href='http://%s/api/authemail?username=%s&code=%s'>http://%s/api/authemail?username=%s&code=%s</a></p>
            <p>请注意，本次验证的有效期为2天。在发送邮件之后的2天内任何时间都可以点击验证。</p>
            <p>如果超过三天还没有点击该链接，则验证将过期。您需要重新请求邮箱验证。</p>
            <p>每个用户每天可以请求10次邮箱验证。如果超过10次，请第二天再试。</p>
        </body>
    </html>"""
    msg_subject = "社区居民求助系统邮箱验证"

    def post(self):
        # get param
        content = self.request.body
        j = json.loads(content)
        if j.has_key("username"):
            username = j["username"]
        else:
            error = {
                "error": "lack params",
                "request": "requestemailauth",
                "error_code": 1
            }
            self.write(json.dumps(error))
            print("lack username")
            return
        # get uid
        user_record = self.application.dbapi.getUserByUserName(username)
        if user_record is None:
            error = {
                "error": "no such user",
                "request": "requestemailauth",
                "error_code": 2
            }
            self.write(json.dumps(error))
            print("no such user")
            return
        uid = user_record["id"]
        # get auth record
        auth_record = self.application.dbapi.getAuth(uid)
        if auth_record is None:
            print "mark 2.1"
            self.application.dbapi.insertAuth(uid)
            print "mark 2.2"
            auth_record = self.application.dbapi.getAuth(uid)
        # if authed, return error
        if auth_record["email_state"] == "authed":
            error = {
                "error": "authed",
                "request": "requestemailauth",
                "error_code": 10001
            }
            self.write(json.dumps(error))
            return
        # find email
        if j.has_key("email"):
            email = j["email"]
            self.application.dbapi.updateAuthData(uid, "email", email)
        elif auth_record["email"] != "":
            email = auth_record["email"]
        else:
            error = {
                "error": "lack params",
                "request": "requestemailauth",
                "error_code": 1
            }
            self.write(json.dumps(error))
            return
        # check request times
        if not self.application.dbapi.checkAuthCnt(uid, "email", 10):
            error = {
                "error": "reach request limits",
                "request": "requestemailauth",
                "error_code": 10002
            }
            self.write(json.dumps(error))
            return
        # update auth count
        self.application.dbapi.incAuthCnt(uid, "email")
        # send email
        code = self.getCode(50)
        if not self.sendAuthEmail(email, username, code):
            error = {
                "error": "send email failed",
                "request": "requestemailauth",
                "error_code": 10003
            }
            self.write(json.dumps(error))
            return
        # insert email code record
        period = 2 * 24 * 3600
        self.application.dbapi.addEmailCode(uid, code, period)
        # update auth state
        self.application.dbapi.updateAuthState(uid, "email", "authing")
        result = {
            "result": "OK"
        }
        self.write(json.dumps(result))

    def getCode(self, num):
        code = ""
        for i in range(0, num):
            code += random.choice(RequestEmailAuthHandler.codechars)
        return code

    def fillMsg(self, username, code):
        msg_content = RequestEmailAuthHandler.msg_content_template % (RequestEmailAuthHandler.host, username, code, RequestEmailAuthHandler.host, username, code)
        return msg_content

    def sendAuthEmail(self, email, username, code):
        msg_content = self.fillMsg(username, code)
        msg = MIMEText(msg_content, _subtype = "html", _charset="utf-8")
        msg["Subject"] = RequestEmailAuthHandler.msg_subject
        msg["From"] = RequestEmailAuthHandler.me
        msg["To"] = email
        try:
            s = smtplib.SMTP()
            s.connect(RequestEmailAuthHandler.mail_host)
            s.login(RequestEmailAuthHandler.mail_user, RequestEmailAuthHandler.mail_pass)
            s.sendmail(RequestEmailAuthHandler.me, email, msg.as_string())
            s.close()
            return True
        except Exception as e:
            return False
            print str(e)
# params:
#   username
#   code
# error_code:
#   prefix: 20000
class AuthEmailHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            username = self.get_argument("username")
            code = self.get_argument("code")
        except:
            error = {
                "error": "lack params",
                "request": "requestemailauth",
                "error_code": 1
            }
            self.write(json.dumps(error))
            return
        # get uid
        user_record = self.application.dbapi.getUserByUserName(username)
        if user_record is None:
            error = {
                "error": "no such user",
                "request": "authemail",
                "error_code": 1
            }
            self.write(json.dumps(error))
            print("no such user")
            return
        uid = user_record["id"]
        if self.application.dbapi.checkEmailCode(uid, code):
            self.application.dbapi.updateAuthState(uid, "email", "authed")
            self.application.dbapi.deleteEmailCode(uid)
            result = {
                "result":"OK"
            }
            self.write(json.dumps(result))
            return
        else:
            error = {
                "error": "email auth code error",
                "request": "authemail",
                "error_code": 20001
            }
            self.write(json.dumps(error))
            return

# 30001 已认证
# 30002 超过验证次数
# 30003 发送短信错误
class RequestPhoneAuthHandler(CHRequestHandler):
    codechars = "0123456789"

    def post(self):
        try:
            j = self.getParams(["username", "phone"])
            uid = self.getUserId(j["username"])
            phone = j["phone"]
        except LackParamsException:
            self.writeError(1, "requestphoneauth")
            return
        except NoUserException:
            self.writeError(2, "requestphoneauth")
            return
        auth_record = self.application.dbapi.getAuth(uid)
        if auth_record is None:
            self.application.dbapi.insertAuth(uid)
            auth_record = self.application.dbapi.getAuth(uid)
        if auth_record["phone_state"] == "authed":
            self.writeError(30001, "requestphoneauth")
            return
        if not self.application.dbapi.checkAuthCnt(uid, "phone", 10):
            self.writeError(30002, "requestphoneauth")
            return
        self.application.dbapi.incAuthCnt(uid, "phone")
        code = self.getCode(6)
        minutes = 10
        if not self.sendSMS(phone, code, minutes):
            self.writeError(30003, "requestphoneauth")
        period = minutes * 60
        self.application.dbapi.addPhoneCode(uid, code, period)
        self.application.dbapi.updateAuthData(uid, "phone", phone)
        self.application.dbapi.updateAuthState(uid, "phone", "authing")
        self.writeOK()


    def getCode(self, num):
        code = ""
        for i in range(0, num):
            code += random.choice(RequestPhoneAuthHandler.codechars)
        return code

    def sendSMS(self, phone, code, minutes):
        datas = [code, minutes]
        return sendTemplateSMS(phone, datas, 1)

from CCPRestSDK import *

accountSid = "aaf98f89476703de01477c05267506ef"
accountToken = "6b34f62bcc964167a6997286bb9a3f2f"
appId = "aaf98f89476703de01477fc1dda307b1"
serverIP = "sandboxapp.cloopen.com"
serverPort = "8883"
softVersion = "2013-12-26"

def sendTemplateSMS(to, datas, temId):
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)
    result = rest.sendTemplateSMS(to, datas, temId)
    if result["statusCode"] == "000000":
        return True
    else:
        return False


# 40001 验证失败
class AuthPhoneHandler(CHRequestHandler):

    def post(self):
        try:
            j = self.getParams(["username", "code"])
            uid = self.getUserId(j["username"])
            code = j["code"]
        except LackParamsException:
            self.writeError(1, "authphone")
            return
        except NoUserException:
            self.writeError(2, "authphone")
            return
        if self.application.dbapi.checkPhoneCode(uid, code):
            self.application.dbapi.updateAuthState(uid, "phone", "authed")
            self.application.dbapi.deletePhoneCode(uid)
            self.writeOK()
            return
        else:
            self.writeError(40001, "authphone")
            return
