from tornado.web import RequestHandler,HTTPError
import session


class BaseHandler(RequestHandler):
    def get_current_user(self):
        print "get_current_user"
        cookie = self.get_secure_cookie('user')
        self._current_user = session.Session.account_by_cookie(cookie)
        if not self._current_user:
            raise HTTPError(403)
        else:
            return self._current_user

    def prepare(self):
        print self.current_user
