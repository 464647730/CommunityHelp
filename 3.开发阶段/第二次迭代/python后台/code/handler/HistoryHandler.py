# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.escape import *
import json

class HistoryHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>historyHandler</p><form action='/api/history' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content='{"name":"test3"}'
		jobj=json.loads(content)
		user = self.application.dbapi.getUserByUserName(jobj['username'])
		if(user is None):
			self.write('{"state":2,"decs":"User not exist"}')
			return
		uid = user['id']
		events=self.application.dbapi.getEventsByUserId(uid)
		for item in events:
			item['longitude'] = float(item['longitude'])
			item['latitude'] = float(item['latitude'])
			item['starttime'] = item['starttime'].strftime('%Y-%m-%d %H:%M:%S')
			if(item['endtime'] is None):
				item['endtime'] = ""
			else:
				item['endtime'] = item['endtime'].strftime('%Y-%m-%d %H:%M:%S')
		#result=self.application.dbapi.getEventsByUserName(jobj['name'])
		supports = self.application.dbapi.getSupportsbyUid(uid)
		for item in supports:
			item['time'] = item['time'].strftime('%Y-%m-%d %H:%M:%S')
		print json_encode(events),json_encode(supports)
		self.write('{"state":1,"events":'+json_encode(events)+',"supports":'+json_encode(supports)+'}')
		return
