import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.escape import *
from sets import Set
import json

class HelpmessageHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>HelpmessageHandler</p><form action='/api/helpmessage' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content='{"username":"test1","message":{"kind":1,"content":"TestContent", "video":"TestAssist","videosign":1,"audeo":"dsds","audiosign":1,"latitude":23.000000,"longitude":23.000000}}'
		jobj=json.loads(content)
		result = self.application.dbapi.addEventByUserName(jobj["username"],jobj["message"])
		self.write(json_encode(result))

		if(jobj['message']['videosign'] =="1"):
			print "test1"
			self.application.util.setVideobyEid(result['eventid'],jobj['video'])

		if(jobj['message']['audiosign'] =="1"):
			print "test2"
			self.application.util.setAudiobyEid(result['eventid'],jobj['audio'])

		"""if(result["state"] == 1):
			eventinfo = self.application.dbapi.getEventandUserByEventId(result['eventid'])
			eventinfo['audio'] = jobj['message']['videosign']
			eventinfo['video'] = jobj['message']['audiosign']
			print '{"type":"help","data":'+json_encode(eventinfo)+'}'
			info = self.application.dbapi.getUserInfobyName(jobj["username"])
			cidlist = self.application.dbapi.getUserCidAround(info["longitude"],info["latitude"],5)
			relativelist = self.application.dbapi.getRelativesCidbyUid(info['id'])
			cidlist.extend(relativelist)
			cidlist =  list(Set(cidlist))
			cidlist.remove(info['cid'])
			print cidlist
			self.application.push.pushToList(cidlist,'{"type":"help","data":'+json_encode(eventinfo)+'}')"""
		if(result["state"] == 1):
			eventinfo = self.application.dbapi.getEventandUserByEventId(result['eventid'])
			eventinfo['audio'] = jobj['message']['videosign']
			eventinfo['video'] = jobj['message']['audiosign']
			pushlist = []
			askuser = self.application.dbapi.getUserInfobyName(jobj["username"])
			relativelist = self.application.dbapi.getRelativesCidbyUid(askuser['id'])
			print relativelist
			pushlist.extend(relativelist)
			friendlist =   self.application.dbapi.getRelativesIdbyUid(askuser['id'])
			hashelpaskuserlist = self.application.dbapi.getHelpersIdbyUid(askuser['id'])
			distance = 3
			special = []
			if(jobj['message']['kind'] ==1):#anquan
				print 1
				special = self.application.dbapi.getAroundbyvocationOrKind(askuser["longitude"],askuser["latitude"],1,4,20,5)
				print special
				pushlist.extend(special)
				aroundhelpers =  self.application.dbapi.getUserAroundbykind(askuser["longitude"],askuser["latitude"],distance,1)
				while len(aroundhelpers) <= 50 and distance <= 7:
					distance +=2
					aroundhelpers=  self.application.dbapi.getUserAroundbykind(askuser["longitude"],askuser["latitude"],distance,1)
				
				
			elif(jobj['message']['kind'] ==2):
				print 2
				aroundhelpers =  self.application.dbapi.getUserAroundbykind(askuser["longitude"],askuser["latitude"],distance,2)
				while len(aroundhelpers) <= 10 and distance <= 7:
					distance +=2
					aroundhelpers =  self.application.dbapi.getUserAroundbykind(askuser["longitude"],askuser["latitude"],distance,2)

			else:#jiankang
				print 3
				special = self.application.dbapi.getAroundbyvocationOrKind(askuser["longitude"],askuser["latitude"],1,5,10,5)
				print special
				pushlist.extend(special)
				aroundhelpers =  self.application.dbapi.getUserAroundbykind(askuser["longitude"],askuser["latitude"],distance,3)
				while len(aroundhelpers) <= 20  and distance <= 5:
					distance +=2
					aroundhelpers = self.application.dbapi.getUserAroundbykind(askuser["longitude"],askuser["latitude"],distance,3)
			
			predictlist = self.application.util.getPushlistByCredit(askuser,aroundhelpers,friendlist,hashelpaskuserlist,0.5,self.application.dbapi)
			print predictlist
			pushlist.extend(predictlist)
			pushlist =  list(Set(pushlist))
			if(askuser['cid'] in pushlist):
				pushlist.remove(askuser['cid'])
			print pushlist
			self.application.push.pushToList(pushlist,'{"type":"help","data":'+json_encode(eventinfo)+'}')
		return

class EventHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>eventHandler</p><form action='/api/event' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content=self.request.body
		#content='{"username":"test4","eventid":1}'
		jobj=json.loads(content)
		uid = self.application.dbapi.getUserByUserName(jobj['username'])["id"]
		helpevent=self.application.dbapi.getEventandUserByEventId(jobj['eventid'])
		print helpevent
		result={}
		if(helpevent):
			helpevent['follows'] = self.application.dbapi.getFollowsByEventId(jobj['eventid'])['count']
			helpevent['helpers'] = len(self.application.dbapi.getHelpersCidbyEid(jobj['eventid']))
			result['event'] = helpevent
			ishelper = self.application.dbapi.checkifUseraddHelper(uid,jobj['eventid'])
			if(ishelper is None):
				if(helpevent['username'] == jobj['username']):
					result['ishelper'] = 1
				else:
					result['ishelper'] = 0
			else:
				result['ishelper'] = 1
			rNamelist = self.application.dbapi.getAllRelativeNamebyUid(helpevent['userid'])
			print rNamelist
			if(uid in rNamelist):
				result['canend'] = 1
			else:
				result['canend'] = 0
			if(self.application.dbapi.getFollow(uid,jobj['eventid']) is None):
				if(helpevent['username'] == jobj['username']):
					result['isfollow'] = 1
				else:
					result['isfollow'] = 0
			else:
				result['isfollow'] = 1
			print result
			result['support']=self.application.dbapi.getSupportsByEventId(jobj['eventid'])
			for support in result['support']:
				user=self.application.dbapi.getUserByUserId(support['usrid'])
				if(user):
					support['username']=user['name'];
					avatar=self.application.util.getAvatarbyUid(support['usrid'])
					support['avatar']=avatar
		self.write(json_encode(result))

'''Yeqin Zheng, 09/07/2014'''
''' Add a helper to an event. Succeed with "1" returned, else with "0". '''
class AddaidHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>AddaidHandler</p><form action='/api/addaid' method='post'><input type='submit' value='submit'></form>")
	def post(self):
		content = self.request.body
		#content = '{"username":"test1","eventid":"4"}'
		j = json.loads(content)

		result = self.application.dbapi.addaidhelper(j['username'], j['eventid'])
		self.write("{'state': " + result + "}")
		uid =self.application.dbapi.getUserByUserName(j['username'])['id']
		self.application.score.joinSupport(uid,self.application.dbapi)


class FinishHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>FinishHandler</p><form action='/api/finish' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content = '{"username":"test1","eventid":1}'
		j = json.loads(content)
		user = self.application.dbapi.getUserByUserName(j['username'])
		event = self.application.dbapi.getEventandUserByEventId(j['eventid'])
		if(event is None):
			self.write("{'state':1}")
			print "event not exist"
			return
		rNamelist = self.application.dbapi.getAllRelativeNamebyUid(event["userid"])
		if(user["id"] not in rNamelist):
			self.write("{'state':2}")
			print "user not relative or itself,can not update sate"
			return
		currenttime = self.application.dbapi.changeEventState(j['eventid'])
		helpers =  self.application.dbapi.getHelperInfoByEid(j['eventid'])
		data = []
		for item in helpers:
			info = {}
			info['username'] = item['username']
			info['uid'] = item['uid']
			data.append(info)
			self.application.dbapi.UpdateInfotimebyUid(item['uid'])
			#data.append("{'username':" + str(item['username']) + ",'uid':"+ str(item['uid'])+"}")
		writedata = {}
		writedata['state'] = 3
		writedata['helpers'] = data
		#push
		pushlist = self.application.dbapi.getFollowerCidByEid(j['eventid'])
		helperlist = self.application.dbapi.getHelpersCidbyEid(j['eventid'])
		pushlist.extend(helperlist)
		relativelist = self.application.dbapi.getRelativesCidbyUid(event["userid"])
		pushlist.extend(relativelist)
		pushlist =  list(Set(pushlist))
		if(user['cid'] in pushlist):
			pushlist.remove(user['cid'])
		pushdata = {}
		data = {}
		pushdata['type'] = "endhelp"
		data['eventid'] = j['eventid']
		data['time'] = currenttime.strftime('%Y-%m-%d %H:%M:%S')
		data['username'] = event['username']
		pushdata['data'] = data
		self.application.push.pushToList(pushlist,json_encode(pushdata))
		self.write(json_encode(writedata))
		print "finsh an event"
		return


class GivecreditHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>GivecreditHandler</p><form action='/api/givecredit' method='post'><input type='submit' value='submit'></form>")
	def post(self):
		content =self.request.body
		#content='{"eventid":4,"helpername":"test2","credit":3}'
		#content='{"eventid":1,"credits":[{"username":"test2","cridit":5},{"username":"test6","cridit":1}]}'
		jobj=json.loads(content)
		result=[]
		event = self.application.dbapi.getEventByEventId(jobj['eventid'])
		askuser = self.application.dbapi.getUserInfobyUid(event['usrid'])
		for issue in jobj["credits"]:
			temp = self.application.dbapi.setCreditByEventIdAndUserName(jobj["eventid"],issue["username"],issue["cridit"])
			result.append({"helpername":issue["username"],"result":temp})
			helper = self.application.dbapi.getUserInfobyName(issue['username'])
			self.application.util.setCreditforHelper(event,askuser,helper,issue["cridit"],self.application.dbapi)
		self.write(str(result))
		self.application.score.giveCredit(event['usrid'],jobj['eventid'],self.application.dbapi)

class QuitaidHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>QuitaidHandler</p><form action='/api/quitaid' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content = '{"username":"oo11o","eventid":5}'
		j = json.loads(content)
		uid = self.application.dbapi.getUserByUserName(j['username'])['id']
		if(self.application.dbapi.getEventByEventId(j['eventid'])['state'] == 1):
			print "current had been end,you can not quit"
			self.write("{'state':3}")
			return

		if(self.application.dbapi.checkifUseraddHelper(uid,j['eventid']) is None):
			print "user " + j['username'] +" do not add the aid first"
			self.write("{'state':2}")
			return
		self.application.dbapi.deleteHelperbyUidEid(uid,j['eventid'])
		print "quit success"
		self.write("{'state':1}") 
		application.score.quitSupport(uid,self.application.dbapi)
		return

class SendsupportHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>SendsupportHandler</p><form action='/api/sendsupport' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		#content='{"username":"test1","eid":4,"message":{"content":"TestssCofffntent"}}'
		jobj=json.loads(content)
		user = self.application.dbapi.getUserByUserName(jobj['username'])
		result=self.application.dbapi.addSupportByEventIdAndUserName(jobj["eid"],jobj["username"],jobj["message"])
		if(result['errorCode'] == 200):
			pushlist = self.application.dbapi.getFollowerCidByEid(jobj['eid'])
			relativelist =self.application.dbapi.getRelativesCidbyUid(user['id'])
			pushlist.extend(relativelist)
			pushlist =  list(Set(pushlist))
			if(user['cid'] in pushlist):
				pushlist.remove(user['cid'])
			eventuser = self.application.dbapi.getUserByEid(jobj['eid'])
			if(eventuser['uid'] !=user['id']):
				pushlist.append(eventuser['cid'])
			datatemp = self.application.dbapi.getSupportBySid(result['supportid'])
			pushdata = {}
			data = {}
			pushdata['type'] = 'aid'
			data['username'] = jobj['username']
			data['content'] = datatemp['content']
			data['time'] = datatemp['time'].strftime('%Y-%m-%d %H:%M:%S')
			data['eventid'] = jobj['eid']
			pushdata['data'] = data
			self.application.push.pushToList(pushlist,json_encode(pushdata))
		self.write(json_encode(result))
		self.application.score.sendSupport(user['id'],self.application.dbapi)

 
class SupportmessageHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("<p>SupportmessageHandler</p><form action='/api/supportmessage' method='post'><input type='submit' value='submit'></form>")

	def post(self):
		content =self.request.body
		content = '{"eventid": 3,"video": "ssssssssssssssss","audio":"ddddd"}'
		j = json.loads(content)
		if('video' in j):
			self.application.util.setVideobyEid(j['eid'],j['video'])
		if('audio' in j):
			self.application.util.setAudiobyEid(j['eid'],j['video']) 
