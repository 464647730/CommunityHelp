# -*- coding: utf-8 -*-
'''Yeqin Zheng, 09/07/2014'''
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.escape import *
import json

''' Add a relation between two users. Succeed with "1" returned, else with "0". '''

class AddrelativesHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>AddrelativesHandler</p><form action='/api/addrelatives' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content = '{"u_name":"test1","r_name":"test5","info":"i am",'kind':}'
		j = json.loads(content)
		row = self.application.dbapi.getRelationByUsername(j['u_name'], j['r_name'])
		if row == 0:
			self.application.dbapi.addtempRelationByUsername(j['u_name'], j['r_name'],j['kind'],j['info'])
			#push data
			cid = self.application.dbapi.getUserByUserName(j['r_name'])['cid']
			pushdata = {}
			datainside = {}
			pushdata['type'] = "invite"
			datainside['username'] = j['u_name']
			datainside['info'] = j['info']
			datainside['type'] = j['kind']
			pushdata['data'] = datainside
			self.application.push.pushToSingle(cid,json_encode(pushdata))
			add_message = {'state': 1}
			print "add relative success"
		else:
			add_message = {'state': 0}
			print "two already has relative relation"
		self.write(add_message)
		return

class CheckrelativesHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>CheckrelativesHandler</p><form action='/api/checkrelatives' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content = '{"username":"test1"}'
		j = json.loads(content)
		userid=self.application.dbapi.getUserByUserName(j['username'])["id"]
		re=self.application.dbapi.CheckRelationbyId(userid)
		if re!=():
			relatives=[]
			for row in re:
				info=self.application.dbapi.getUsermessegeByUserId(row["cid"])
				info['kind'] = row['kind']
				info['avatar'] = self.application.util.getAvatarbyUid(info['id'])
				#relatives.append('{"info":'+str(info)+',"avatar":'+self.application.util.getAvatarbyUid(info['id'])+'}')
				relatives.append(info)
			data={'state':1,'relatives':relatives}
		else:
			data={'state':1,'relatives':'[]'}
		self.write(json_encode(data))

'''Yeqin Zheng, 09/07/2014'''
''' Delete a relation between two users. Succeed with "1" returned, else with "0". '''
class DeleterelativesHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>DeleterelativesHandler</p><form action='/api/deleterelatives' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content = '{"username1":"ooo","username2":"11oo"}'
		j = json.loads(content)
		row = self.application.dbapi.getRelationByUsername(j['username1'],j['username2'])
		if row == 0 :
			delete_message = {'state': 0}
			print "two has no relations"
		else :
			self.application.dbapi.deleteRelationByUsername(j['username1'],j['username2'])
			print "delete relations success"
			delete_message = {'state': 1}

		self.write(delete_message)
		return

class AgreerelativesHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>AgreerelativesHandler</p><form action='/api/agreerelatives' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content = '{"u_name":"ooo","c_name":"11oo","kind": ,"agree":1(1同意，0不同意)}'
		j = json.loads(content)
		user = self.application.dbapi.getUserByUserName(j['u_name'])
		cid = self.application.dbapi.getUserByUserName(j['c_name'])['id']
		if(j['agree'] == "1"):
			self.application.dbapi.deletetemprelation(user['id'],cid)
			self.application.dbapi.addRelationByUid(user['id'],cid,j['kind'])
			print "agree 1"
			pushdata = {}
			pushdata['type'] = "agree"
			data = {}
			data['userid'] = user['id']
			data['username'] = user['name']
			data['type'] = j['kind']
			self.application.push.pushToSingle(user['cid'],json_encode(pushdata))
			state = {'state':1}
		else:
			self.application.dbapi.deletetemprelationwithkind(user['id'],cid,j['kind'])
			print "agree 0"
			state = {'state':1}
		self.write(json_encode(state))
		return

class ValidationHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>ValidationHandler</p><form action='/api/getvalidation' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content = '{"username":"test6"}'
		j = json.loads(content)
		user = self.application.dbapi.getUserByUserName(j['username'])
		validations = self.application.dbapi.gettemprelationbyCid(user['id'])
		result={}
		if len(validations):
			result['state'] = 1
			for item in validations:
				print item
				item['u_name'] = self.application.dbapi.getUserByUserId(item['uid'])['name']
		else:
			result['state'] = 0
		result['validations'] = validations
		self.write(json_encode(result))
		return
