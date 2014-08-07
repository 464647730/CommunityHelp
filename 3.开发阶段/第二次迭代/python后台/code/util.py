# -*- coding: utf-8 -*-
import json,os,base64
import datetime

class util:
	def setAvatar(self,username,filestring,dbapi):
		userid=dbapi.getUserByUserName(username)['id']
		avatar=open(os.path.abspath('./static/avatar/'+str(userid)+".png"),"wb")
		avatar.write(base64.standard_b64decode(filestring))
		avatar.close()

	def getAvatar(self,username,dbapi):
		userid=dbapi.getUserByUserName(username)['id']
		avatar=open(os.path.abspath('./static/avatar/'+str(userid)+".png"),"rb")
		result=""
		result=base64.standard_b64encode(avatar.read())
		avatar.close()
		return result

	def setAvatarbyUid(self,uid,filestring):
		avatar=open(os.path.abspath('./static/avatar/'+str(uid)+".png"),"wb")
		avatar.write(base64.standard_b64decode(filestring))
		avatar.close()

	def getAvatarbyUid(self,uid):
		avatar=open(os.path.abspath('./static/avatar/'+str(uid)+".png"),"rb")
		result=""
		result=base64.standard_b64encode(avatar.read())
		avatar.close()
		return result

	def setVideobyEid(self,uid,videostring):
		newdir ='./static/Video/'+str(uid)
		os.mkdir(newdir)
		video=open(os.path.abspath('./static/Video/'+str(uid)+'/'+str(uid)+'.3gp'),"wb")
		video.write(base64.standard_b64decode(videostring))
		video.close()

	def setAudiobyEid(self,uid,videostring):
		newdir = './static/Audio/'+str(uid)
		os.mkdir(newdir)
		audio=open(os.path.abspath('./static/Audio/'+str(uid)+'/'+str(uid)+'.amr'),"wb")
		audio.write(base64.standard_b64decode(videostring))
		audio.close()

	def setCreditforHelper(self,event,askuser,helper,credit,dbapi):

		credit = float(credit)
		credit *= (2 * 0.1) 
		T_preCredit = dbapi.getpreviousEvent(askuser['id'], helper['id']) 
		
		helperReputation = helper['credit']
		Reputation = 0

		#helperReputation = T_preCredit['credit']
		
		if helper['time'] == None:
			Reputation = (credit + helperReputation) / 2
		else:
			timeInterval = (datetime.datetime.now() - helper['time']).days
			if credit <= 0.4:
				helper['beta'] /= 2 
				helper['gama'] /= 2 
				factor = 1 / pow(timeInterval * 2 + 1, 1 / 3.0)
				Reputation = helper['beta'] * factor * helperReputation + (1 - helper['beta'] * factor) * credit
			else:
				helper['beta'] += helper['gama'] 
				if helper['beta'] > 0.5:
					helper['beta'] = 0.5 
				factor = 1 / pow(timeInterval + 1, 1 / 3.0)
				Reputation = (1 - helper['beta']) * factor * helperReputation + (1 - ((1 - helper['beta']) * factor)) * credit
				
		dbapi.updateUserCredit(helper['id'], Reputation)
		dbapi.updateUserbetagama(helper['id'], helper['beta'],helper['gama'])

		if T_preCredit == None:
			dbapi.insertpreviousEvent(askuser['id'], helper['id'], credit, event['endtime'])
		else:
			dbapi.updatepreviousEvent(askuser['id'], helper['id'], credit, event['endtime'])


	def getPushlistByCredit(self,askuser,aroundhelpers,friendlist,hashelpaskuserlist,percent,dbapi):
		pushlist = []
		lastpushlist = []
		for helper in aroundhelpers:
			jv = 0.0
			helperReputation = 0.0
			hisCr = 0.0
			if friendlist is not None:
				friend_helper_list = []
				for friend in friendlist:
					if dbapi.getpreviousEvent(friend['id'], helper['id']) is not None:
						friend_helper_list.append(friend)
				if friend_helper_list is not None:
					tv = []
					fv = []
					for f in friend_helper_list:
						T_preCredit = dbapi.getpreviousEvent(f['id'], helper['id'])
						fv.append(T_preCredit['credit'])
						CmmNds = []
						for hashelpaskuser in hashelpaskuserlist:
							if dbapi.getpreviousEvent(f['id'], hashelpaskuser['id']) is not None:
								CmmNds.append(hashelpaskuser)

						para1 = 0.0
						para2 = 0.0
						para3 = 0.0

						if CmmNds is not None:
							for Mi in CmmNds:
								T_preCredit1 = dbapi.getpreviousEvent(askuser['id'], Mi['id'])
								T_preCredit2 = dbapi.getpreviousEvent(f['id'], Mi['id'])
								para1 += (T_preCredit1['credit'] * T_preCredit2['credit'])
								para2 += pow(T_preCredit1['credit'], 2.0)
								para3 += pow(T_preCredit2['credit'], 2.0)
							temp = pow(para2, 1 / 2.0) * pow(para3, 1 / 2.0)
							if temp == 0:
								temp = 0.000001
							tv.append(para1 / temp)
					jv = 0.0
					sumOf_tv = 0.0
					sumOf_fv = 0.0
					for TV in tv:
						sumOf_tv += TV
					for FV in fv:
						sumOf_fv += FV
					if sumOf_tv != 0.0:
						jv = (sumOf_fv * sumOf_tv) / sumOf_tv

			helperReputation = helper['credit']
			T_preCredit3 = dbapi.getpreviousEvent(askuser['id'], helper['id'])
			if T_preCredit3 is not None:
				hisCr = T_preCredit3['credit']

			last_credit = jv + helperReputation + hisCr
			pushlist.append((helper['name'],helper['cid'], last_credit))

		pushlist.sort(key = lambda x: x[2], reverse = True)
		count = 0
		for person in pushlist:
			if count >= (len(pushlist) * percent):
				break
			lastpushlist.append(person)
			count += 1

		pushlist = []
		for item in lastpushlist:
			pushlist.append(item[1])
		return pushlist
