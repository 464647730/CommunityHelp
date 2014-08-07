__author__ = 'Administrator'

import tornado.web
import json

class NoUserException(Exception):
    def __init__(self):
        pass

class LackParamsException(Exception):
    def __init__(self):
        pass

class CHRequestHandler(tornado.web.RequestHandler):
    def getUserId(self, username):
        record = self.application.dbapi.getUserByUserName(username)
        if record is None:
            raise NoUserException()
        return record["id"]

    def getParams(self, essentials = []):
        j = json.loads(self.request.body)
        for k in essentials:
            if not j.has_key(k):
                raise LackParamsException()
        return j

    def writeError(self, error_code, apiname):
        error = {
            "result": "error",
            "request": apiname,
            "error_code": error_code
        }
        self.write(json.dumps(error))

    def writeOK(self):
        result = {
            "result": "ok"
        }
        self.write(result)

