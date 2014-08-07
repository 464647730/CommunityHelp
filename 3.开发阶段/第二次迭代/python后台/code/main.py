import tornado.ioloop
import tornado.web
import tornado.httpserver
import os,MySQLdb,dbapi,util,score
from handler import *
from push import *
from xml.dom.minidom import parse,parseString

class app(tornado.web.Application):
	def __init__(self):
		settings = {
			"static_path": os.path.join(os.path.dirname(__file__), "static"),
			"debug": True
		}
		handlers=[
			(r"/api/login",UserHandler.LoginHandler),
			(r"/api/register",UserHandler.RegisterHandler),
			(r"/api/userauthentication",UserHandler.AuthenHandler),
			(r"/api/logout",UserHandler.LogoutHandler),
			(r"/api/cancel",UserHandler.CancelHandler),
			(r"/api/updatecid",UserHandler.UpdateCid),
			(r"/api/search",UserHandler.SearchHandler),
			(r"/api/getavatar",UserHandler.GetAvatarHandler),
			
			(r"/api/checkrelatives",RelativesHandler.CheckrelativesHandler),
			(r"/api/deleterelatives",RelativesHandler.DeleterelativesHandler),
			(r"/api/addrelatives",RelativesHandler.AddrelativesHandler),
			(r"/api/agreerelatives",RelativesHandler.AgreerelativesHandler),
			(r"/api/getvalidation",RelativesHandler.ValidationHandler),

			(r"/api/history",HistoryHandler.HistoryHandler),

			(r"/api/helpmessage",EventHandler.HelpmessageHandler),
			(r"/api/supportmessage",EventHandler.SupportmessageHandler),
			(r"/api/finish",EventHandler.FinishHandler),
			(r"/api/givecredit",EventHandler.GivecreditHandler),
			(r"/api/addaid",EventHandler.AddaidHandler),
			(r"/api/sendsupport",EventHandler.SendsupportHandler),
			(r"/api/quitaid",EventHandler.QuitaidHandler),
			(r"/api/event",EventHandler.EventHandler),

			(r"/api/getuserinfo",UserInfoHandler.GetUserInfoHandler),
			(r"/api/updateuserinfo",UserInfoHandler.UpdateUserInfoHandler),

			(r"/api/getAround",GetArroundEvent.GetArroundEvent),

			(r"/api/startfollow",FollowHandler.startFollowHandler),
			(r"/api/cancelfollow",FollowHandler.cancelFollowHandler),
			
			(r"/api/thirdpartylogin",ThirdPartHandlers.ThirdPartyLoginHandler),
			(r"/api/thirdpartyremoveaccount",ThirdPartHandlers.ThirdPartyRemoveAccountHandler),
			(r"/api/thirdpartyfilluserinfo",ThirdPartHandlers.ThirdPartyFillUserInfoHandler),

			(r"/api/authstate", Authorize.AuthStateHandler),
			(r"/api/requestemailauth", Authorize.RequestEmailAuthHandler),
			(r"/api/authemail", Authorize.AuthEmailHandler),
			(r"/api/requestphoneauth", Authorize.RequestPhoneAuthHandler),
			(r"/api/authphone", Authorize.AuthPhoneHandler)]
		tornado.web.Application.__init__(self,handlers,**settings)
		self.dbapi=dbapi.dbapi()
		self.util=util.util()
		self.push = Push()
		self.score=score.score()
		

if __name__=="__main__":
	server=tornado.httpserver.HTTPServer(app())
	server.listen(8080)
	tornado.ioloop.IOLoop.instance().start()
