from tornado.web import RequestHandler,HTTPError
import session
from pymongo import MongoClient
conn = MongoClient()
db = conn.hr

class BaseHandler(RequestHandler):
    def get_current_user(self):
        # print "get_current_user"
        cookie = self.get_secure_cookie('user')
        self._current_user = session.Session.account_by_cookie(cookie)
        if not self._current_user:
            raise HTTPError(403)
        else:
            return self._current_user

    def prepare(self):
        print self.current_user

    def user_auth(self):
        user = db.admin_user.find_one({"username":self.current_user})
        is_admin = user.get('is_admin')
        second_level = user.get('second_level')
        first_level = user.get('first_level')
        base_level = user.get('base_level')
        if is_admin:
            auth = {'admin':1,"base":1,"first":1,"second":1}
        else:
            if second_level:
                auth = {'admin': 0, "base": 0, "first": 0, "second": 0}
            elif first_level:
                auth = {'admin': 0, "base": 0, "first": 0, "second": 1}
            elif base_level:
                auth = {'admin': 0, "base": 0, "first": 1, "second": 1}
        return auth
