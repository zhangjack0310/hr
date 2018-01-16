import redis
import settings





redis_client = redis.Redis(db=1)


class Session(object):

    @classmethod
    def new(cls, account, expire=60*60):
        if account:
            key = settings.SESSION_NAME.format(account)
            redis_client.setex(key, account, expire)
            return str(account)

    @classmethod
    def rm(cls, account):
        key = settings.SESSION_NAME.format(account)
        if key:
            redis_client.delete(key)

    @classmethod
    def account_by_cookie(cls, cookie):
        if cookie:
            key = settings.SESSION_NAME.format(cookie)
            if redis_client.get(key):
                return str(cookie)
            else:
                return False
        else:
            return False
