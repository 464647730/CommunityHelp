# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.escape import *
import json

class UpdateUserInfoHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>UpdateUserInfoHandler</p><form action='/api/updateuserinfo' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content = '{"username":"dasda1","changemessage":{"age":15,"illness":"我是小啊小苹果"}}'
		j = json.loads(content)
		user = self.application.dbapi.getUserByUserName(j['username'])
		if(user is None):
			self.write("{'state':1}")
			print "username not exist"
			return
		if('avatar' in j):
			self.application.util.setAvatar(j['username'],j['avatar'],self.application.dbapi)
		result = self.application.dbapi.updateUserinfo(user['id'],j['changemessage'])
		if(isinstance(result,list)):
			state = 1
		else:
			state =2
		self.write("{'state':"+ str(state)+"}")
		print("UpdateUserInfo success")
		return

class GetUserInfoHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>GetUserInfoHandler</p><form action='/api/getuserinfo' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content = '{"username":"test1"}'
		j = json.loads(content)
		user = self.application.dbapi.getUserByUserName(j['username'])
		if(user is None):
			self.write("{'state':1}")
			print "username not exist"
			return
		result = self.application.dbapi.getUsermessegeByUserId(user['id'])
		result['credit'] = 5 * result['credit']
		scorelimit = self.application.score.getRankByScore(result['score'])
		
		result['scoreMin'] = scorelimit['scoreMin']
		result['scoreMax'] = scorelimit['scoreMax']
		result['scoreLevel'] = scorelimit['scoreLevel']
		print result
		self.write("{'result':"+ json_encode(result)+"}")
		print("GetUserInfo success")
		return
