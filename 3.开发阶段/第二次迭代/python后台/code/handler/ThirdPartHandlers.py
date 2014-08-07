# coding: utf-8
# Filename: handlers.py
__author__ = 'Administrator'

import tornado.web
import json,os,base64
import urllib
from CHRequestHandler import CHRequestHandler, LackParamsException, NoUserException

# 2014-07-17
#
# post: access_token, platform
# return: result
# actions:
# visit get_token_info
#     check for binding
#     create new user
#     bind user
#     update user state
# 我需要与前后台协商，除了本地登录之外，在增加第三方专用的返回值。这里就将就一下
# error code
#   50001 访问授权api失败
#   50002 不支持的平台
#   50003 授权过期
class ThirdPartyLoginHandler(CHRequestHandler):
	platformapi = { "sinaweibo": "https://api.weibo.com/oauth2/get_token_info" }
	requestname = "thirdpartylogin"

	def post(self):
		try:
			j = self.getParams(["platformname", "access_token", "latitude", "longitude"])
		except LackParamsException:
			self.writeError(1, ThirdPartyLoginHandler.requestname)
			return
		url = ThirdPartyLoginHandler.platformapi.get(j["platformname"])
		if url is None:
			self.writeError(50002, ThirdPartyLoginHandler.requestname)
			return
		data = "access_token=" + j["access_token"]
		try:
			resultstr = urllib.urlopen(url, data).read()
		except IOError:
			self.writeError(50001, ThirdPartyLoginHandler.requestname)
			return
		# 解析返回值，这里依旧只考虑了新浪微博
		result = json.loads(resultstr)
		expire_in = result["expire_in"]
		# 如果令牌超时，则驳回请求
		if expire_in <= 0:
			# 返回state：1
			self.writeError(50003, ThirdPartyLoginHandler.requestname)
			return
		# 第三方不需要在本系统中设置用户名，因此自动生成一个作为第三方用户的唯一标识
		username = "*" + j["platformname"] + ("%i" % result["uid"])
		# 这里做简单处理：直接将星号+platform+uid作为用户名，不设密码
		# 其他用户不允许第一个符号是星号。一般的用户名只允许出现字母，数字，空格，和下划线。
		# 首先检查是否已经注册过
		try:
			uid = self.getUserId(username)
		except NoUserException:
			newUser = {"username": username,
					   "kind": 1,
					   "password": "",
					   "cardid": 0,
					   "realname": "",
					   "sex": 0,
					   "age": 0,
					   "address": "",
					   "phone": "",
					   "vocation": 3,
					   "illness": ""}
			uid = self.application.dbapi.register(newUser)
			avatar=open(os.path.abspath('./static/avatar/default.png'),"rb");
			filestring=base64.standard_b64encode(avatar.read())
			self.application.util.setAvatarbyUid(uid,filestring)
			self.application.score.userRegister(uid,self.application.dbapi)
		self.application.dbapi.updateUseLBS(j['latitude'],j['longitude'],uid)
		self.application.dbapi.updateUserstate(uid, 1) # 登录状态为数字1
		self.writeOK()
		return

# 在第三方登录成功之后，第三方用户状态就与本地用户相同了。这里的登出过程也几乎没有区别
class ThirdPartyLogoutHandler(tornado.web.RequestHandler):
	# 数据库的所有操作都没有进行用户是否已经登录的检查。
	# 鉴于这种检查时普遍操作，可能会作为任何一项需要特权的操作的前置操作，仅仅需要修改少数类，因此这里不做检查，等待小组长修复该bug
	# 这里需要将访问方式改为post。之前考虑失误。显然应该是post
	def post(self):
		# 这与正常的登出一模一样。直接copy代码。
		# 这里用到了username。按照我的预想，是不需要username的。但是第一版可以简单设计。
		# 这需要我修改几处anroid代码
		# 其他人采用json格式传输数据。我这里并没有采用，而是直接使用参数传递。
		username = "*" + self.get_argument("platform") + self.get_argument("uid")
		print("username: " + username)
		# 因为假设所有的特权操作都经过了检查，因此不必考虑用户不存在的情况
		record = self.application.dbapi.getUserByUserName(username)
		uid = record["id"]
		self.application.dbapi.updateUserstate(uid, 0)
		self.write("{'state':1}")
		self.write("Third Party Logout Test")

# 50001 访问平台授权服务器错误
# 50002 不支持的平台
# 50003 授权超时
class ThirdPartyRemoveAccountHandler(CHRequestHandler):
	platformapi = { "sinaweibo": "https://api.weibo.com/oauth2/get_token_info" }
	requestname = "thirdpartyremoveaccount"

	# 与前面一个一样，这里的get也是不对的，需要改为post
	def post(self):
		try:
			j = self.getParams(["platformname", "access_token"])
		except LackParamsException:
			self.writeError(1, ThirdPartyLoginHandler.requestname)
			return
		url = ThirdPartyLoginHandler.platformapi.get(j["platformname"])
		if url is None:
			self.writeError(50002, ThirdPartyLoginHandler.requestname)
			return
		data = "access_token=" + j["access_token"]
		try:
			resultstr = urllib.urlopen(url, data).read()
		except IOError:
			self.writeError(50001, ThirdPartyLoginHandler.requestname)
			return
		# 解析返回值，这里依旧只考虑了新浪微博
		result = json.loads(resultstr)
		expire_in = result["expire_in"]
		# 如果令牌超时，则驳回请求
		if expire_in <= 0:
			# 返回state：1
			self.writeError(50003, ThirdPartyLoginHandler.requestname)
			return
		# 第三方不需要在本系统中设置用户名，因此自动生成一个作为第三方用户的唯一标识
		username = "*" + j["platformname"] + ("%i" % result["uid"])
		# 这里做简单处理：直接将星号+platform+uid作为用户名，不设密码
		# 其他用户不允许第一个符号是星号。一般的用户名只允许出现字母，数字，空格，和下划线。
		# 首先检查是否已经注册过
		try:
			uid = self.getUserId(username)
		except NoUserException:
			self.writeError(2, ThirdPartyRemoveAccountHandler.requestname)
			return
		self.application.dbapi.cancelUser(uid)
		# 用户已删除，这是返回登录成功的返回值，暗示了用户已删除
		print("delete user")
		self.writeOK()

class ThirdPartyFillUserInfoHandler(tornado.web.RequestHandler):
	def post(self):
		username = "*" + self.get_argument("platform") + self.get_argument("uid")
		newUserInfo = {
			"sex": self.get_argument("sex"),
			"address": self.get_argument("address")
		}
		user = self.application.dbapi.getUserByUserName(username)
		if(user is None):
			self.write("{'state':1}")
			print "username not exist"
			return
		print("username: " + username)
		print("sex: " + newUserInfo["sex"])
		print("address: " + newUserInfo["address"])
		result = self.application.dbapi.updateUserinfo(user['id'], newUserInfo)
		self.write("{'result':"+ str(result)+"}")
		print("UpdateUserInfo success")
