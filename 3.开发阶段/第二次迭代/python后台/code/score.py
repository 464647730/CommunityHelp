import os,xml.etree.ElementTree as ET
import time
from datetime import datetime
class score:
	def __init__(self):
		_config=ET.parse(os.path.abspath("./static/config.xml"))
		root=_config.getroot()
		levels=root.findall("./score/level")
		ops=root.findall("./ops/op")

		self.config=dict()
		for level in levels:
			num=int(level[0].text)
			minScore=int(level[1].text)
			maxScore="INF" if level[2].text=="INF" else int(level[2].text)


			self.config[num]=dict()
			self.config[num]['min']=minScore
			self.config[num]['max']=maxScore

		self.ops=dict()
		for op in ops:
			cond=int(op[0].text)
			score_op=int(op[1].text)
			score_max="INF" if op[2].text=="INF" else int(op[2].text)

			self.ops[cond]=dict()
			self.ops[cond]['op']=score_op
			self.ops[cond]['max']=score_max

	def getRankByScore(self,s):
		for num in self.config:
			if (self.config[num]['max']=="INF" or s<=self.config[num]['max']) and s>=self.config[num]['min']:
				result=dict()
				result['scoreMin']=self.config[num]['min']
				result['scoreMax']=self.config[num]['max']
				result['scoreLevel']=num
				return result
		print "error in getRankByScore("+str(s)+")"

	# 1:new user login for the first time +5/5
	# 2:user login for the first time every day +1/1
	# 3:caller give helper credit +2/50
	# 4:helper join in support +3/Infinity
	# 5:helper send support message +1/30
	# 6:user online for more than 12 hours a day +2/2

	# 7:helper earn the highest credit in a event +5/Infinity
	# allow more than one helper earn it in the same event

	# 8:send harmful support message -10/Infinity
	# 9:send useless event message -20/Infinity
	# 10:helper quit the event while the event does not end -1/Infinity
	# 11:caller give no credit to the helper after the event end for five days -10/infinity

	def updateScoreByCase(self,uid,cond,dbapi):
		if cond in self.ops:
			info = dbapi.getScoreInfoById(uid)
			score_op = self.ops[cond]["op"]
			if info is not None:
				name = "score"+str(cond)
				if self.ops[cond]["max"]=="INF":
					dbapi.operateScoreById(uid,score_op)
					dbapi.operateScoreInfoById(uid,cond,score_op)
				elif abs(info[name]+self.ops[cond]["op"]) <= abs(self.ops[cond]["max"]):
					dbapi.operateScoreById(uid,score_op)
					dbapi.operateScoreInfoById(uid,cond,score_op)
				else:
					return False

			return True
		else:
			return False

	def userRegister(self,uid,dbapi):
		dbapi.addScoreInfoById(uid)
		return self.updateScoreByCase(uid,1,dbapi)

	def userLogin(self,uid,dbapi):
		info = dbapi.getScoreInfoById(uid)
		if info is not None:
			if info['login_time'].strftime("%Y-%m-%d %H:%M:%S") == "2000-01-01 00:00:00":
				dbapi.setScoreTimeById(uid,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
				return self.updateScoreByCase(uid,2,dbapi)
			else:
				return False
		else:
			return False

	def giveCredit(self,uid,eid,dbapi):
		self.updateScoreByCase(uid,3,dbapi)
		#condition 7
		helpers = dbapi.getGreatestHelperId(eid)
		for helper in helpers:
			self.updateScoreByCase(helper['usrid'],7,dbapi)


	def joinSupport(self,uid,dbapi):
		return self.updateScoreByCase(uid,4,dbapi)

	def sendSupport(self,uid,dbapi):
		return self.updateScoreByCase(uid,5,dbapi)

	def checkOnlineHours(self,uid,dbapi):
		info = dbapi.getScoreInfoById(uid)
		if info is not None:
			if datetime.fromtimestamp(time.time()).hour - info['login_time'].hour >= 12:
				return self.updateScoreByCase(uid,6,dbapi)

	def quitSupport(self,uid,dbapi):
		return self.updateScoreByCase(uid,10,dbapi)

if __name__ == '__main__':
	test=score()
	print test.getRankByScore(700)