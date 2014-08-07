# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.escape import *
import json,os,base64

class RegisterHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>RegisterHandler</p><form action='/api/register' method='post'><input type='submit' value='submit'></form>")	

	def post(self):
		content =self.request.body
		#content = '{"username": "test1","password": "1","kind": 1, "cardid":"test" ,"realname":"1","sex":1,"age":1, "address":"1","illness":"1","phone":"11"}'
		j = json.loads(content)
		if(self.application.dbapi.getUserByUserName(j['username']) is not None):
			self.write("{'state':1}")
			print "username exist"
			return
		if(self.application.dbapi.getInfoBycardid(j['cardid']) is not None):
			self.write("{'state':2}")
			print "cardid exist"
			return
		uid = self.application.dbapi.register(j)
		self.write("{'state':3}")
		print("Register success")

		if('file' in j):
			self.application.util.setAvatar(j['username'],j['file'],self.application.dbapi)
		else:
			avatar=open(os.path.abspath('./static/avatar/default.png'),"rb");
			filestring=base64.standard_b64encode(avatar.read())
			self.application.util.setAvatar(j['username'],filestring,self.application.dbapi)
		self.application.score.userRegister(uid,self.application.dbapi)
		return

class LoginHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>LoginHandler</p><form action='/api/login' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content = self.request.body
		#content = '{"username":"12","password":"1","latitude":23.000000,"longitude":23.000000}'
		j = json.loads(content)
		if(j['username'].strip()=='' or j['username'].strip()[0]== '*'):
			self.write("{'state':1}")
			print "username is illegal"
			return

		user = self.application.dbapi.getUserByUserName(j['username'])
		if(user is None):
			self.write("{'state':1}")
			print "username not exist"
			return
		if(user["password"]!= j['password']):
			self.write("{'state':2}")
			print "passwd incorrect"
			return
		if("latitude" in j):
			self.application.dbapi.updateUseLBS(j['latitude'],j['longitude'],user['id'])
		self.application.dbapi.updateUserstate(user['id'],1)
		result = {}
		result['state'] = 3
		result['userid'] = user['id']
		self.write(json_encode(result))
		print("Login success")
		self.application.score.userLogin(user['id'],self.application.dbapi)
		return

class UpdateCid(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>UpdateCid</p><form action='/api/updatecid' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content = self.request.body
		j = json.loads(content)
		user = self.application.dbapi.getUserByUserName(j['username'])
		if(user is None):
			self.write("{'state':2}")
			print "username not exist"
			return
		self.application.dbapi.UpdateCidByuid(j['cid'],user['id'])
		self.write("{'state':1}")
		print("Login success")
		return

class LogoutHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>LogoutHandler</p><form action='/api/logout' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		print content
		#content = '{"username":"11oo"}'
		j = json.loads(content)
		uid = self.application.dbapi.getUserByUserName(j['username'])['id']
		self.application.dbapi.updateUserstate(uid,0)
		self.write("{'state':1}")
		print("Logout success")
		self.application.score.checkOnlineHours(uid,self.application.dbapi)
		return

class AuthenHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>AuthenHandler</p><form action='/api/userauthentication' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		#self.write("AuthenHandler")
		print "start"
		content='{"username":"test1","message":{"kind":1}}'
		jobj=json.loads(content)
		askuser = self.application.dbapi.getUserInfobyName(jobj["username"])
		print self.application.dbapi.getAroundbyvocationOrKind(askuser["longitude"],askuser["latitude"],1,5,10,5)
		#print askuser
		aroundhelpers = self.application.dbapi.getUserAroundbykind(askuser["longitude"],askuser["latitude"],5,jobj['message']['kind'])
		#print aroundhelpers
		friendlist =   self.application.dbapi.getRelativesIdbyUid(askuser['id'])
		#print friendlist
		hashelpaskuserlist = self.application.dbapi.getHelpersIdbyUid(askuser['id'])
		#print hashelpaskuserlist
		pushlist = self.application.util.getPushlistByCredit(askuser,aroundhelpers,friendlist,hashelpaskuserlist,0.2,self.application.dbapi)
		#print pushlist	
		print "lall"
		return


class CancelHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>CancelHandler</p><form action='/api/cancel' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content = self.request.body
		print content
		#content = '{"username":"test","password":"test"}'
		j = json.loads(content)
		if(j['username'].strip()=='' ):
			self.write("{'state':1}")
			print "username is null"
			return
		user = self.application.dbapi.getUserByUserName(j['username'])
		if(user is None):
			self.write("{'state':1}")
			print "username not exist,can not cancel"
			return
		if(user["password"]!= j['password']):
			self.write("{'state':2}")
			print "passwd incorrect,can not cancel"
			return
		self.application.dbapi.cancelUser(user['id'])
		self.write("{'state':3}")
		print("cancel success")
		return

class SearchHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>SearchHandler</p><form action='/api/search' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		print content
		#content = '{"searchtype":"2","fromage":"20","endage":"30"}'
		j = json.loads(content)
		if(j['searchtype'] == "exactSearch"):
			user = self.application.dbapi.getUserByUserName(j['username'])
			if(user is not None):
				users = []
				username = {}
				username['username'] = user['name']
				users.append(username)
				result ={}
				result['state'] = 1
				result['users'] = users
			else:
				result =  {'state': 0}
		elif(j['searchtype'] == "keywordSearch"):
			result = self.application.dbapi.searchUserbySexAgeKind(j)
		else:
			result = self.application.dbapi.getUserAround(j['longitude'],j['latitude'],5)
		print result
		self.write(json_encode(result))
		print("Login success")
		return

class GetAvatarHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>CancelHandler</p><form action='/api/getavatar' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		print content
		#content = '{"uid":"test"，"username":"testname"}'
		j = json.loads(content)
		result = {}
		if('uid' in j):
			result['avatar'] = self.application.util.getAvatarbyUid(j['uid'])
		else:
			result['avatar'] = self.application.util.getAvatar(j['username'],self.application.dbapi)
		self.write(json_encode(result))
		return
