# -*- coding: utf-8 -*-
import MySQLdb,json
import thread,time

#in init function please change the config to fit your own requirement
#fetchone(): return type: None/dict
#fetchall(): return type: tuple(may be empty tuple)
#all function below return a value or a list

class dbapi:
	def __init__(self):
		self.host="localhost"
		self.user="comhelp"
		self.passwd="20140629"
		#self.user="root"
		#self.passwd="root"
		self.dbname="community"
		self.charset="utf8"
		self.db=MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.dbname,charset=self.charset)
		thread.start_new_thread(self.setDailyTask, ())

	def getUserByUserId(self,userid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from user where id=%s"
		param=(userid,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	def getUserByUserName(self,username):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from user where name=%s"
		param=(username,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	def getHelperInfoByEid(self,eid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select user.name as username,user.id as uid from helper,user where helper.eid=%s and helper.usrid = user.id"
		param=(eid,)
		cursor.execute(sql,param)
		result=cursor.fetchall()
		cursor.close()
		return result

	def updateUserstate(self,uid,state):
		cursor = self.db.cursor()
		sql = "update user set state = %s where id = %s"
		param =(state,uid)
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()
		return

	def updateUserCredit(self,uid,credit):
		cursor = self.db.cursor()
		sql = "update info set credit = %s where id = %s"
		param = (credit,uid)
		try:
			cursor.execute(sql,param)
			self.db.commit()
		except:
			self.db.rollback()
		cursor.close()
		return

	def updateUseLBS(self,latitude,longitude,uid):
		cursor = self.db.cursor()
		sql = "update info set latitude = %s , longitude = %s where id = %s"
		param =(latitude,longitude,uid)
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()
		return

	#get user userfull info in user+info
	#pre con: user exist
	#after: return a dict result include all info of user
	def getUserAllinfobyName(self,name):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		uid = self.getUserByUserName(name)['id']
		return self.getUsermessegeByUserId(uid)

	#get user all info in user+info
	#pre con: user exist
	#after: return a dict result include all info of user
	def getUserInfobyName(self,name):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "select * from user,info where user.name = %s and user.id = info.id"
		param = (name,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	def getUserInfobyUid(self,uid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "select * from user,info where user.id = %s and user.id = info.id"
		param = (uid,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	def CheckRelationbyId(self,userid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from relation where usrid=%s"
		param=(userid,)
		cursor.execute(sql,param)
		result=cursor.fetchall()
		cursor.close()
		return result

	def getUsermessegeByUserId(self,userid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select user.id,user.name,info.name as realname,info.sex,info.age,info.address,info.illness,info.credit,info.score,phone from user,info where user.id=%s and info.id=%s"
		param=(userid,userid)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	def getUserByEid(self,eid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select cid,user.id as uid from user,event where event.id= %s and event.usrid=user.id"
		param=(eid,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	def getEventByEventId(self,eventid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from event where id=%s"
		param=(eventid,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	def getEventandUserByEventId(self,eventid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="""select user.name as username,user.id as userid,content,starttime as time,event.kind as kind,event.id as eventid, event.latitude as latitude,event.longitude as longitude,Video as video, audio from event,user
				where event.id=%s and user.id = event.usrid"""
		param=(eventid,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		result['time'] = result['time'].strftime('%Y-%m-%d %H:%M:%S')
		result['longitude'] = float(result['longitude'])
		result['latitude'] = float(result['latitude'])
		cursor.close()
		return result

	def getEventsByUserId(self,userid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from event where usrid=%s"
		param=(userid,)
		cursor.execute(sql,param)
		result=cursor.fetchall()
		cursor.close()
		return list(result)

	def getEventsByUserName(self,username):
		user=self.getUserByUserName(username)
		if(not user):
			return []
		return self.getEventsByUserId(user["id"])

	def getSupportBySid(self,sid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from support where id = %s"
		param=(sid,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	#get supports by uid
	def getSupportsbyUid(self,uid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select user.name,support.eid,support.content,support.time from support,user where usrid = user.id and usrid = %s"
		param=(uid,)
		cursor.execute(sql,param)
		result=cursor.fetchall()
		cursor.close()
		return list(result)

	#get supports by username
	def getSupportsbyUsername(self,username):
		user=self.getUserByUserName(username)
		if(not user):
			return []
		return self.getSupportsbyUid(user["id"])

	#insert follow uid->eid
	def insertFollow(self,uid,eid):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		cursor.execute("select now()")
		currentTime=cursor.fetchone()
		sql = "insert into follow(eid,usrid,time) values(%s,%s,%s)"
		param = (eid,uid,currentTime['now()'])
		state = 1
		try:
			cursor.execute(sql,param)
			self.db.commit()
			state = 1
		except:
			self.db.rollback()
			state = 0
		cursor.close()
		return state

	#delect follow uid->eid
	def delectFollow(self,uid,eid):
		cursor = self.db.cursor()
		sql = "delete from follow where eid = %s and usrid = %s"
		param = (eid,uid)
		state = 1
		try:
			cursor.execute(sql,param)
			self.db.commit()
			state = 1
		except:
			self.db.rollback()
			state = 0
		cursor.close()
		return state

	#get follow by uid,eid
	#if no recode,rerun None;else return dir
	def getFollow(self,uid,eid):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "select * from follow where eid = %s and usrid = %s"
		param = (eid,uid)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	def getFollowerCidByEid(self,eid):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "select user.cid from follow,user where eid = %s and user.id = follow.usrid"
		param = (eid,)
		cursor.execute(sql,param)
		result = []
		for row in cursor.fetchall():
			result.append(row['cid'])
		cursor.close()
		return result

	def getFollowsByEventId(self,eid):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "select count(*) as count from follow where eid = %s"
		param = (eid,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result


	def getHelpersCidbyEid(self,eid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select cid from helper,user where eid = %s and helper.usrid = user.id"
		param=(eid,)
		cursor.execute(sql,param)
		result = []
		for row in cursor.fetchall():
			result.append(row['cid'])
		cursor.close()
		return result

	def getRelativesCidbyUid(self,uid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select user.cid from relation,user where usrid = %s and relation.cid = user.id"
		param=(uid,)
		cursor.execute(sql,param)
		result = []
		for row in cursor.fetchall():
			result.append(row['cid'])
		cursor.close()
		return result
	
	def getRelativesIdbyUid(self,uid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select cid as id from relation where usrid = %s"
		param=(uid,)
		cursor.execute(sql,param)
		result = cursor.fetchall()
		cursor.close()
		return list(result)
	
	def getHelpersIdbyUid(self,uid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select DISTINCT helper.usrid as id from event,helper where event.usrid = %s and event.id = helper.eid"
		param=(uid,)
		cursor.execute(sql,param)
		result = cursor.fetchall()
		cursor.close()
		return list(result)
	
	#check if cardid exist
	#exist return dict
	#not exist return none
	def getInfoBycardid(self,cardid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from info where cardid=%s"
		param=(cardid,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	#register a new user
	#pre condiction:no user.name,info.cardid duplicate
	#after : insert new user,new info
	def register(self,content):
		cursor = self.db.cursor()
		sql = "insert into user(name,kind,password) values(%s,%s,%s)"
		param = (content["username"],content["kind"],content["password"])
		cursor.execute(sql,param)
		self.db.commit()
		
		cursor.execute('SELECT LAST_INSERT_ID()')
		result=cursor.fetchone()
		print result[0]

		sql = "insert into info(id,cardid,name,sex,age,illness,score,phone,vocation) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		param = (result[0],content["cardid"],content["realname"],content["sex"],content["age"],content["illness"],0,content["phone"],content["vocation"])
		cursor.execute(sql,param)
		self.db.commit()
				
		cursor.close()
		return result[0]

	def getRelationByUserId(self, u_id, r_id):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="SELECT * FROM relation WHERE usrid = '" + u_id + "' AND cid = '" + r_id + "'"
		cursor.execute(sql)
		row = int(cursor.rowcount)
		cursor.close()
		return row

	#update user cid by uid
	def UpdateCidByuid(self,cid,uid):
		cursor = self.db.cursor()
		sql ="update user set cid = NULl where cid = %s"
		param = (cid,)
		cursor.execute(sql,param)
		self.db.commit()

		sql = "update user set cid = %s where id = %s"
		param = (cid,uid)
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()
		return
	
	def UpdateInfotimebyUid(self,uid):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		cursor.execute("select now()")
		currentTime=cursor.fetchone()
		sql ="update info set time = %s where id = %s"
		print currentTime['now()']
		param = (currentTime['now()'],uid)
		try:
			cursor.execute(sql,param)
			self.db.commit()
		except:
			self.db.rollback()
		cursor.close()
		return
	def updateUserbetagama(self,uid,beta,gama):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql ="update info set beta = %s, gama = %s where id = %s"
		param = (beta,gama,uid)
		try:
			cursor.execute(sql,param)
			self.db.commit()
		except:
			self.db.rollback()
		cursor.close()
		return

	#get all relativeName by user.id
	#return a list contain all relations(including uid)
	def getAllRelativeNamebyUid(self,uid):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "select * from relation where usrid = %s and kind = %s"
		param = (uid,1)
		rlist = []
		rlist.append(uid)
		cursor.execute(sql,param)
		for row in cursor.fetchall():
			rlist.append(row["cid"])
		return rlist

	# change a event sate to 1
	#in order to end a event
	def changeEventState(self,eid):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		cursor.execute("select now()")
		currentTime=cursor.fetchone()
		sql ="update event set state= %s ,endtime = %s where id = %s"
		param = (1,currentTime['now()'],eid)
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()
		return currentTime['now()']

	#cancle a user by user(id)
	#pre condiction: uid exist
	#after:delete all record of this user
	def cancelUser(self,uid):
		cursor = self.db.cursor()
		sql = "delete from user where id = %s"
		param = (uid,)
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()
		return

	#get all events around user(latitude,longitude) inside distance
	#pre con:user(latitude,longitude) exist,distance >=0
	#after:return a list contain event info or []
	def getEventAround(self,lon,lat,distance):
		cursor = self.db. cursor(cursorclass=MySQLdb.cursors.DictCursor)
		#sql = "select round(6378.138*2*asin(sqrt(pow(sin( (event.latitude*pi()/180-(%s)*pi()/180)/2),2)+cos(event.latitude*pi()/180)*cos((%s)*pi()/180)* pow(sin( (event.longitude*pi()/180-(%s)*pi()/180)/2),2)))) from event"
		#param = (lat,lat,lon)
		sql = """select event.id,user.name,event.kind,event.content,event.starttime,video,audio from event,user where 
				 exists(select id from event where event.latitude <= (%s+1) and event.latitude >= (%s-1) and longitude <= (%s+1) and longitude>=(%s-1))
				 and event.usrid = user.id
				 and event.state = 0
				 and round(6378.138*2*asin(sqrt(pow(sin( (event.latitude*pi()/180-(%s)*pi()/180)/2),2)+cos(event.latitude*pi()/180)*cos((%s)*pi()/180)* pow(sin( (event.longitude*pi()/180-(%s)*pi()/180)/2),2)))) < %s 
				 ORDER BY starttime DESC limit 15"""
		param = (lat,lat,lon,lon,lat,lat,lon,distance)
		cursor.execute(sql,param)
		result = []
		for row in cursor.fetchall():
			row['starttime'] = row['starttime'].strftime('%Y-%m-%d %H:%M:%S')
			result.append(row)
		cursor.close()
		return result

	#get all user(cid) around latitude,longitude inside distance(use for push)
	#pre condiction：lon,lat exist,distance>=0
	#after :return a list coantain user.cid or []
	def getUserCidAround(self,lon,lat,distance):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = """select user.cid from user,info where
				exists(select id from info where latitude <= (%s+1) and latitude >= (%s-1) and longitude <= (%s+1) and longitude>=(%s-1))
				and user.state = 1
				and user.id = info.id
				and round(6378.138*2*asin(sqrt(pow(sin( (info.latitude*pi()/180-(%s)*pi()/180)/2),2)+cos(info.latitude*pi()/180)*cos((%s)*pi()/180)* pow(sin( (info.longitude*pi()/180-(%s)*pi()/180)/2),2)))) < %s"""
		param = (lat,lat,lon,lon,lat,lat,lon,distance)
		cursor.execute(sql,param)
		result = []
		for row in cursor.fetchall():
			result.append(row['cid'])
		cursor.close()
		return result

	def getUserAround(self,lon,lat,distance):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = """select user.name as name from user,info where
				exists(select id from info where latitude <= (%s+1) and latitude >= (%s-1) and longitude <= (%s+1) and longitude>=(%s-1))
				and user.id = info.id
				and round(6378.138*2*asin(sqrt(pow(sin( (info.latitude*pi()/180-(%s)*pi()/180)/2),2)+cos(info.latitude*pi()/180)*cos((%s)*pi()/180)* pow(sin( (info.longitude*pi()/180-(%s)*pi()/180)/2),2)))) < %s"""
		param = (lat,lat,lon,lon,lat,lat,lon,distance)
		cursor.execute(sql,param)
		sqlre = cursor.fetchall()
		cursor.close
		result = []
		if(sqlre):
			for row in sqlre:
				info = {}
				info['username'] = row['name']
				result.append(info)
			data={'state':1,'users':result}
		else:
			data={'state':0}#the user not exist,return state 0
		#result=json.dumps(data)
		return data
	
	def getUserAroundbykind(self,lon,lat,distance,kind):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		if(kind == 1):
			sql = """select user.id as id,user.name as name,info.credit as credit ,user.cid as cid from user,info where
				exists(select id from info where latitude <= (%s+1) and latitude >= (%s-1) and longitude <= (%s+1) and longitude>=(%s-1))
				and user.id = info.id
				and (age>=20 and age <=40)
				and round(6378.138*2*asin(sqrt(pow(sin( (info.latitude*pi()/180-(%s)*pi()/180)/2),2)+cos(info.latitude*pi()/180)*cos((%s)*pi()/180)* pow(sin( (info.longitude*pi()/180-(%s)*pi()/180)/2),2)))) < %s""" 
			param = (lat,lat,lon,lon,lat,lat,lon,distance)
		elif(kind == 2):
			sql ="""select user.id as id,user.name as name,info.credit as credit ,user.cid as cid from user,info where
				exists(select id from info where latitude <= (%s+1) and latitude >= (%s-1) and longitude <= (%s+1) and longitude>=(%s-1))
				and user.id = info.id
				and (age>=20 and age <=50)
				and round(6378.138*2*asin(sqrt(pow(sin( (info.latitude*pi()/180-(%s)*pi()/180)/2),2)+cos(info.latitude*pi()/180)*cos((%s)*pi()/180)* pow(sin( (info.longitude*pi()/180-(%s)*pi()/180)/2),2)))) < %s"""
			param = (lat,lat,lon,lon,lat,lat,lon,distance)
		else:
			sql = """select user.id as id,user.name as name,info.credit as credit ,user.cid as cid from user,info where
				exists(select id from info where latitude <= (%s+1) and latitude >= (%s-1) and longitude <= (%s+1) and longitude>=(%s-1))
				and user.id = info.id
				and round(6378.138*2*asin(sqrt(pow(sin( (info.latitude*pi()/180-(%s)*pi()/180)/2),2)+cos(info.latitude*pi()/180)*cos((%s)*pi()/180)* pow(sin( (info.longitude*pi()/180-(%s)*pi()/180)/2),2)))) < %s"""
			param = (lat,lat,lon,lon,lat,lat,lon,distance)
		cursor.execute(sql,param)
		sqlre = cursor.fetchall()
		return list(sqlre)
	
	def getAroundbyvocationOrKind(self,lon,lat,vocation,u_kind,vocation_limit,u_limit):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = """(select user.cid as cid from user,info where
				exists(select id from info where latitude <= (%s+1) and latitude >= (%s-1) and longitude <= (%s+1) and longitude>=(%s-1))
				and user.id = info.id
				and (vocation = %s)
				order by round(6378.138*2*asin(sqrt(pow(sin( (info.latitude*pi()/180-(%s)*pi()/180)/2),2)+cos(info.latitude*pi()/180)*cos((%s)*pi()/180)* pow(sin( (info.longitude*pi()/180-(%s)*pi()/180)/2),2)))) asc limit %s)
				UNION
				(select user.cid as cid from user,info where
				exists(select id from info where latitude <= (%s+1) and latitude >= (%s-1) and longitude <= (%s+1) and longitude>=(%s-1))
				and user.id = info.id
				and (kind = %s)
				order by round(6378.138*2*asin(sqrt(pow(sin( (info.latitude*pi()/180-(%s)*pi()/180)/2),2)+cos(info.latitude*pi()/180)*cos((%s)*pi()/180)* pow(sin( (info.longitude*pi()/180-(%s)*pi()/180)/2),2)))) asc limit %s)"""
		param = (lat,lat,lon,lon,vocation,lat,lat,lon,vocation_limit,lat,lat,lon,lon,u_kind,lat,lat,lon,u_limit)
		cursor.execute(sql,param)
		cursor.close
		result = []
		for row in cursor.fetchall():
			result.append(row['cid'])
		cursor.close()
		return result
	
	#update user info by username,sex,age,phone,address,illness
	#pre cond:uid exist
	#after: update user info for what it pass
	def updateUserinfo(self,uid,message):
		cursor = self.db.cursor()
		result = []
		if("realname" in message):
			sql = "update info set name = %s where id = %s"
			param = (message["realname"],uid)
			try:
				cursor.execute(sql,param)
				self.db.commit()
			except:
				self.db.rollback()
				return {"state":2,"desc":"db access error username"}
			result.append({"state":1,"desc":"update username success"})
		if("sex" in message):
			sql = "update info set sex = %s where id = %s"
			param = (message["sex"],uid)
			try:
				cursor.execute(sql,param)
				self.db.commit()
			except:
				self.db.rollback()
				return {"state":2,"desc":"db access error sex"}
			result.append({"state":1,"desc":"update sex success"})
		if("age" in message):
			sql = "update info set age = %s where id = %s"
			param = (message["age"],uid)
			try:
				cursor.execute(sql,param)
				self.db.commit()
			except:
				self.db.rollback()
				return {"state":2,"desc":"db access error age"}
			result.append({"state":1,"desc":"update age success"})
		if("phone" in message):
			sql = "update info set phone = %s where id = %s"
			param = (message["phone"],uid)
			try:
				cursor.execute(sql,param)
				self.db.commit()
			except:
				self.db.rollback()
				return {"state":2,"desc":"db access error age"}
			result.append({"state":1,"desc":"update age success"})
		if("address" in message):
			sql = "update info set address = %s where id = %s"
			param = (message["address"],uid)
			try:
				cursor.execute(sql,param)
				self.db.commit()
			except:
				self.db.rollback()
				return {"state":2,"desc":"db access error address"}
			result.append({"state":1,"desc":"update address success"})
		if("illness" in message):
			sql = "update info set illness = %s where id = %s"
			param = (message["illness"],uid)
			try:
				cursor.execute(sql,param)
				self.db.commit()
			except:
				self.db.rollback()
				return {"state":2,"desc":"db access error illness"}
			result.append({"state":1,"desc":"update illness success"})
		cursor.close()
		return result

	'''Yeqin Zheng, 09/07/2014'''
	def getRelationByUsername(self, u_name, r_name):
		result = self.getUserByUserName(u_name)
		u_id = str(result["id"])
		result = self.getUserByUserName(r_name)
		r_id = str(result["id"])
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="SELECT * FROM relation WHERE usrid = '" + u_id + "' AND cid = '" + r_id + "'"
		cursor.execute(sql)
		row = int(cursor.rowcount)
		cursor.close()
		return row

	def deleteRelationByUsername(self, u_name, r_name):
		result = self.getUserByUserName(u_name)
		u_id = str(result["id"])
		result = self.getUserByUserName(r_name)
		r_id = str(result["id"])
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="DELETE FROM relation WHERE usrid = '" + u_id + "' AND cid = '" + r_id + "'"
		cursor.execute(sql)
		self.db.commit()
		cursor.close()

	def addRelationByUid(self, u_id, r_id,kind):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="INSERT INTO relation(usrid, cid, kind) VALUES(%s,%s,%s)"
		param=(u_id,r_id,kind)
		cursor.execute(sql,param)
		self.db.commit()
		sql="INSERT INTO relation(usrid, cid, kind) VALUES(%s,%s,%s)"
		param=(r_id,u_id,kind)
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()


	def addtempRelationByUsername(self, u_name, r_name,kind,info):
		result = self.getUserByUserName(u_name)
		u_id = str(result["id"])
		result = self.getUserByUserName(r_name)
		r_id = str(result["id"])
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="INSERT INTO temprelation (uid, cid, kind,info) VALUES(%s,%s,%s,%s)"
		param=(u_id,r_id,kind,info)
		try:
			cursor.execute(sql,param)
			self.db.commit()
		except:
			self.db.rollback()
		cursor.close()

	def deletetemprelation(self,uid,cid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="delete from temprelation where uid = %s and cid =%s"
		param=(uid,cid)
		try:
			cursor.execute(sql,param)
			self.db.commit()
		except:
			self.db.rollback()
		cursor.close()
		return

	def deletetemprelationwithkind(self,uid,cid,kind):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="delete from temprelation where uid = %s and cid =%s and kind = %s"
		param=(uid,cid,kind)
		try:
			cursor.execute(sql,param)
			self.db.commit()
		except:
			self.db.rollback()
		cursor.close()
		return

	def gettemprelationbyCid(self,cid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from temprelation where cid =%s"
		param=(cid,)
		cursor.execute(sql,param)
		result = cursor.fetchall()
		return list(result)

	def addaidhelper(self, u_name, e_id):
		result = self.getUserByUserName(u_name)
		u_id = str(result["id"])
		result = self.getEventByEventId(e_id)
		if(self.checkifUseraddHelper(u_id,e_id) is not None):
			print "already add in,do not need add agagin"
			return "2"
		if result["state"] == 1:
			print "current has benn end"
			return "3"
		else:
			cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
			sql="INSERT INTO helper (eid, usrid) VALUES ('" + e_id + "', '" + u_id + "')"
			cursor.execute(sql)
			self.db.commit()
			cursor.close()
			print "user " +u_name +" add in "+ e_id
			return "1"

	def checkifUseraddHelper(self,userid,eventid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from helper where eid=%s and usrid = %s"
		param=(eventid,userid)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		print result
		return result

	def deleteHelperbyUidEid(self,uid,eid):
		cursor=self.db.cursor()
		sql="delete from helper where eid = %s and usrid = %s"
		param=(eid,uid)
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()
		return


	#Anton Zhong
	def getUserIdByUserName(self,username):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select id from user where name=%s"
		param=(username,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	def addEventByUserName(self,username,message):
		usrid=self.getUserIdByUserName(username)
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		if(not usrid):
			return {"state":2,"errorDesc":"No Such User: "+username}
		else:
			if(not("kind" in message and "content" in message)):
				return {"state":3,"errorDesc":"Messge Incomplete"}
			else:
				cursor.execute("select now()")
				currentTime=cursor.fetchone()
				#sql = "select * from event where usrid = %s and kind = %s and latitude = %s and longitude = %s and TIMESTAMPDIFF(MINUTE,%s,starttime)<= 10"
				#param = (usrid["id"],message["kind"],message['latitude'],message['longitude'],currentTime['now()'])
				#cursor.execute(sql,param)
				#if(cursor.fetchall()):
				if(False):
					return {"state":4,"errorDesc":"cannnot send the same message in 10 minute"}
				sql="insert into event (usrid,kind,state,content,starttime,latitude,longitude) values (%s,%s,%s,%s,%s,%s,%s)"
				param=(usrid["id"],message["kind"],0,message["content"],currentTime['now()'],message['latitude'],message['longitude'])
				cursor.execute(sql,param)
				self.db.commit()

				cursor.execute("select last_insert_id()")
				eid = cursor.fetchone()["last_insert_id()"]
				if(message['videosign'] =="1" and message['audiosign'] =="1"):
					self.UpdateEventVideoAndAudio(eid)
				elif(message['videosign'] =="1" and message['audiosign'] =="0"):
					self.UpdateEventVideo(eid)
				elif(message['videosign'] =="0" and message['audiosign'] =="1"):
					self.UpdateEventAudio(eid)
				return {"state":1,"errorDesc":"","eventid":eid}
		cursor.close()

	def UpdateEventVideoAndAudio(self,eid):
		cursor = self.db.cursor()
		sql = "update event set video = %s,audio = %s where id = %s"
		param = ('http://114.215.133.61:8080/static/Video/'+str(eid)+'/'+str(eid)+'.3gp','http://114.215.133.61:8080/static/Audio/'+str(eid)+'/'+str(eid)+'.amr',eid)
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()
		return

	def UpdateEventVideo(self,eid):
		cursor = self.db.cursor()
		sql = "update event set video = %s where id = %s"
		param = ('http://114.215.133.61:8080/static/Video/'+str(eid)+'/'+str(eid)+'.3gp',eid)
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()
		return

	def UpdateEventAudio(self,eid):
		cursor = self.db.cursor()
		sql = "update event set audio = %s where id = %s"
		param = ('http://114.215.133.61:8080/static/Audio/'+str(eid)+'/'+str(eid)+'.amr',eid)
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()
		return
	#07/09

	#seach user by sex,age,kind and return the row of table user
	# it has 8 options
	def searchUserbySexAgeKind(self,content):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		if('sex' in content):
			if('fromage' in content):
				if('kind' in content):
					sql="select user.id from user,info where info.sex=%s and info.age>=%s and info.age<=%s and user.kind=%s and user.id = info.id"
					param=(content['sex'],content['fromage'],content['endage'],content['kind'])
				else:
					sql="select user.id from user,info where info.sex=%s and info.age>=%s and info.age<=%s and user.id = info.id"
					param=(content['sex'],content['fromage'],content['endage'])
			else:
				if('kind' in content):
					sql="select user.id from user,info where info.sex=%s and user.kind=%s and user.id = info.id"
					param=(content['sex'],content['kind'])
				else:
					sql="select info.id from info,user where info.sex=%s and user.id = info.id"
					param=(content['sex'],)
		else:
			if('fromage' in content):
				if('kind' in content):
					sql="select user.id from user,info where info.age>=%s and info.age<=%s and user.kind=%s and user.id = info.id"
					param=(content['fromage'],content['endage'],content['kind'])
				else:
					sql="select user.id from user,info where info.age>=%s and info.age<=%s and user.id = info.id"
					param=(content['fromage'],content['endage'])
			else:
				if('kind' in content):
					sql="select user.id from user,info where user.kind=%s and user.id = info.id"
					param=(content['kind'],)
				else:
					data=[{'state':0}]#input is null return state 0
					result=json.dumps(data)
					return result
		cursor.execute(sql,param)
		result1=cursor.fetchall()
		cursor.close()
		if(result1):
			userlist=[]
			for x in result1:
				info = {}
				info['username'] = self.getUserByUserId(x['id'])['name']
				userlist.append(info)
			data={'state':1,'users':userlist}#return the user table successly
		else:
			data={'state':0}#the user not exist,return state 0
		return data

	#update the password by userid and userpassword
	def UpdatePassword(self,content):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		if(content['passwd']):
			sql="update user set passwd=%s where id=%s"
			param=(content['passwd'],content['id'])
			cursor.execute(sql,param)
			self.db.commit()
			data=[{'state':1}]#update success return state 1
			result=json.dumps(data)
			return result
			
		else:
			data=[{'state':0}]#input is null return state 0
			result=json.dumps(data)
			return result
		cursor.close()


	#Anton Zhong
	def getHelperByEventIdAndUserName(self,eid,username):
		usrid=self.getUserIdByUserName(username)
		#No such user return none
		if(not usrid):
			return None
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from helper where eid=%s and usrid=%s"
		param=(eid,usrid["id"])
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	def checkHelperByEventIdAndUserName(self,eid,username):
		usrid=self.getUserIdByUserName(username)
		if(not usrid):
			return False
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select usrid from helper where eid=%s"
		param=(eid,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		if(not result):
			return False
		return True

	def addSupportByEventIdAndUserName(self,eid,username,message):
		#if(not self.checkHelperByEventIdAndUserName(eid,username)):
		#	return {"errorCode":403,"errorDesc":"No Such Helper"+str(username)+" in event "+str(eid)}
		if(not ("content" in message) ):
			return {"errorCode":403,"errorDesc":"Messge Incomplete"}
		else:
			cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
			cursor.execute("select now()")
			currentTime=cursor.fetchone()
			sql="insert into support (eid,usrid,content,time) values (%s,%s,%s,%s)"
			param=(eid,self.getUserIdByUserName(username)["id"],message["content"],currentTime['now()'])
			cursor.execute(sql,param)
			self.db.commit()
			cursor.execute("select last_insert_id()")
			result=cursor.fetchone()
			cursor.close()
			return {"errorCode":200,"errorDesc":"","supportid":result["last_insert_id()"]}

	def setCreditByEventIdAndUserName(self,eid,username,credit):
		if(not self.checkHelperByEventIdAndUserName(eid,username)):
			return {"errorCode":403,"errorDesc":"No Such Helper "+str(username)+" in event "+str(eid)}
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="update helper set credit = %s where eid=%s and usrid=%s"
		usrid=self.getUserIdByUserName(username)
		param=(credit,eid,usrid["id"])
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()
		#self.updateUserCreditScore(eid,usrid["id"],credit)
		return {"errorCode":200,"errorDesc":""}
	#07/10

	def getSupportsByEventId(self,eid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from support where eid=%s ORDER BY time DESC"
		param=(eid,)
		cursor.execute(sql,param)
		result=[]
		for item in cursor.fetchall():
			item['time'] = item['time'].strftime('%Y-%m-%d %H:%M:%S')
			result.append(item)
		return result

	#get record from previousEvent
	#after:return None or dict
	def getpreviousEvent(self,askid,helperid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from previousEvent where askid=%s  and helperid = %s"
		param=(askid,helperid)
		cursor.execute(sql,param)
		result = cursor.fetchone()
		return result
		
	#insert new record into previousEvent
	#after:the table insert a new record
	def insertpreviousEvent(self,askid,helperid,credit,eventstarttime):
		cursor = self.db.cursor()
		sql = "insert into previousEvent(askid,helperid,time,credit) values(%s,%s,%s,%s)"
		param = (askid,helperid,eventstarttime,credit)
		try:
			cursor.execute(sql,param)
			self.db.commit()
		except:
			self.db.rollback()
		cursor.close()
		return

	#update the record in previousEvent
	#after:update the record of (askid,helpid)
	def updatepreviousEvent(self,askid,helperid,credit,eventstarttime):
		cursor = self.db.cursor()
		sql = "update previousEvent set credit = %s, time = %s where askid = %s and helperid = %s"
		param = (credit,eventstarttime,askid,helperid)
		try:
			cursor.execute(sql,param)
			self.db.commit()
		except:
			self.db.rollback()
		cursor.close()
		return

	def insertAuth(self, uid):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "insert into auth(id, email_state, phone_state) values(%s, 'unauth', 'unauth')"
		param = (uid,)
		succeed = True
		try:
			cursor.execute(sql, param)
			self.db.commit()
		except Exception as e:
			succeed = False
			print(e)
		finally:
			cursor.close()
		return succeed

	def getAuth(self, uid):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "select * from auth where id = %s"
		param = (uid,)
		cursor.execute(sql, param)
		result = cursor.fetchone()
		cursor.close()
		return result

	def updateAuthState(self, uid, kind, newState):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "update auth set %s_state = '%s' where id = %%s" % (kind, newState)
		param = (uid,)
		cursor.execute(sql, param)
		self.db.commit()
		cursor.close()

	def updateAuthData(self, uid, kind, value):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "update auth set %s = %%s where id = %%s" % kind
		param = (value, uid)
		cursor.execute(sql, param)
		self.db.commit()
		cursor.close()

	# if in limit, return True.
	def checkAuthCnt(self, uid, kind, limits):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "select * from auth_cnt where id = %%s and kind = \"%s\"" % kind
		param = (uid,)
		cursor.execute(sql, param)
		result = cursor.fetchone()
		if result is None:
			sql = "insert into auth_cnt(id, kind, cnt) values(%%s, \"%s\", 0)" % kind
			cursor.execute(sql, param)
			cursor.close()
			return True
		sql = "select * from auth_cnt where id = %%s and kind = \"%s\" and cnt <= %s" % (kind, limits)
		cursor.execute(sql, param)
		result = cursor.fetchone()
		cursor.close()
		if result is None:
			return False
		else:
			return True

	def incAuthCnt(self, uid, kind):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "update auth_cnt set cnt = cnt + 1 where id = %%s and kind = \"%s\"" % kind
		param = (uid,)
		cursor.execute(sql, param)
		self.db.commit()
		cursor.close()

	def addEmailCode(self, uid, code, period):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "select * from email_code where id = %s"
		param = (uid,)
		cursor.execute(sql, param)
		result = cursor.fetchone()
		if result is None:
			sql = "insert into email_code(id, code, expire_in) values(%%s, %%s, unix_timestamp() + %s)" % period
			param = (uid, code)
		else:
			sql = "update email_code set code = %%s, expire_in = unix_timestamp() + %s where id = %%s" % period
			param = (code, uid)
		cursor.execute(sql, param)
		self.db.commit()
		cursor.close()

	def checkEmailCode(self, uid, code):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "select * from email_code where id = %s and code = %s and expire_in > unix_timestamp()"
		param = (uid, code)
		cursor.execute(sql, param)
		result = cursor.fetchone()
		if result is None:
			return False
		else:
			return True

	def deleteEmailCode(self, uid):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "delete from email_code where id = %s"
		param = (uid,)
		cursor.execute(sql, param)
		self.db.commit()
		cursor.close()

	def setDailyTask(self):
		while True:
			time.sleep(24 * 3600)
			self.clearAuthTempData()

	def clearAuthTempData(self):
		# clear auth_cnt table
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "delete from auth_cnt"
		cursor.execute(sql)
		self.db.commit()
		# clear out date email code records
		sql = "delete from email_code where expire_in < unix_timestamp()"
		cursor.execute(sql)
		self.db.commit()
		cursor.close()

	def addPhoneCode(self, uid, code, period):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "select * from phone_code where id = %s"
		param = (uid,)
		cursor.execute(sql, param)
		result = cursor.fetchone()
		if result is None:
			sql = "insert into phone_code(id, code, expire_in) values(%%s, %%s, unix_timestamp() + %s)" % period
			param = (uid, code)
		else:
			sql = "update phone_code set code = %%s, expire_in = unix_timestamp() + %s where id = %%s" % period
			param = (code, uid)
		cursor.execute(sql, param)
		self.db.commit()
		cursor.close()
		pass

	def checkPhoneCode(self, uid, code):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "select * from phone_code where id = %s and code = %s and expire_in > unix_timestamp()"
		param = (uid, code)
		cursor.execute(sql, param)
		result = cursor.fetchone()
		if result is None:
			return False
		else:
			return True

	def deletePhoneCode(self, uid):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "delete from phone_code where id = %s"
		param = (uid,)
		cursor.execute(sql, param)
		self.db.commit()
		cursor.close()

	def operateScoreById(self,uid,score_op):
		cursor = self.db.cursor()
		if score_op > 0:
			sql = "update info set score = score+%s where id = %s"
		else:
			sql = "update info set score = score-%s where id = %s"
		param = (abs(score_op),uid)
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()

	def addScoreInfoById(self,uid):
		cursor = self.db.cursor()
		sql = "insert into score_info(id,login_time) values(%s,%s)"
		param = (uid,"2000-01-01 00:00:00")
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()

	def operateScoreInfoById(self,uid,cond,score_op):
		cursor = self.db.cursor()
		if score_op > 0:
			sql = "update score_info set score"+str(cond)+" = score"+str(cond)+"+%s where id = %s" 
		else:
			sql = "update score_info set score"+str(cond)+" = score"+str(cond)+"-%s where id = %s" 
		param = (abs(score_op),uid)
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()

	def getScoreInfoById(self,uid):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "select * from score_info where id = %s"
		param = (uid,)
		cursor.execute(sql, param)
		result = cursor.fetchone()
		if result is None:
			return None
		else:
			return result

	def setScoreTimeById(self,uid,curTime):
		cursor = self.db.cursor()
		sql = "update score_info set login_time = %s where id = %s" 
		param = (curTime,uid)
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()

	def getGreatestHelperId(self,eid):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "select max(credit) from helper where eid = %s"
		param = (eid,)
		cursor.execute(sql, param)
		cre = cursor.fetchone()
		cre = cre['max(credit)']
		sql = "select usrid from helper where eid = %s and credit = %s"
		param = (eid,cre)
		cursor.execute(sql, param)
		result = cursor.fetchall()
		return result


	def __del__(self):
		self.db.close()
