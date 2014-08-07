# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import json

class startFollowHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>startFollowHandler</p><form action='/api/startfollow' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content='{"eid":2,"username":"test2"}'
		j=json.loads(content)
		user=self.application.dbapi.getUserByUserName(j['username'])["id"]
		if(user):
			if(self.application.dbapi.getFollow(user,j['eid'])):
				data={'state':3,'desc':"have been followed"}#have  been followed
				result=json.dumps(data)
			else:
				self.application.dbapi.insertFollow(user,j['eid'])
				data={'state':1,'desc':"start follow success"}#start follow success
				result=json.dumps(data)
		else:
			data={'state':2,'desc':"user no exist"}#user no exist
			result=json.dumps(data)
		self.write(result)
		return

class cancelFollowHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>cancelFollowHandler</p><form action='/api/cancelfollow' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content='{"eid":2,"username":"test2"}'
		j=json.loads(content)
		user=self.application.dbapi.getUserByUserName(j['username'])["id"]
		if(user):
			if(self.application.dbapi.getFollow(user,j['eid'])):
				self.application.dbapi.delectFollow(user,j['eid'])
				data={'state':1,'desc':"delete follow success"}#delete follow success
				result=json.dumps(data)
			else:
				data={'state':3,'desc':"have no follow"}#have no follow
				result=json.dumps(data)
		else:
			data={'state':2,'desc':"user no exist"}#user no exist
			result=json.dumps(data)
		self.write(result)
		return
