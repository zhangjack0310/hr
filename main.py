#coding:utf-8
import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
from service import form_total_data, is_validate_user
from data.bubble import form_bubble_data,form_department_bubble_data
from pymongo import MongoClient
from utils import BaseHandler
import os
import session
conn = MongoClient()
db = conn.hr
import json
from settings import settings

class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    # @tornado.web.authenticated
    def get(self):
        people = db.base.find({"事业部":"总部","一级部门":"财务部","二级部门":"财务部"},{"_id":0})
        result = list(people)
        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps(result, ensure_ascii=False))


class GetdataHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    # @tornado.web.authenticated
    def get(self):
        based = self.get_argument('based', u"总部")
        firstd = self.get_argument('firstd', u'财务部')
        secondd = self.get_argument('secondd', u'财务部')
        if based == u'事业部':  # 什么都没选
            query = {"based":u"总部","firstd":u"财务部", "secondd":u"财务部"}
            people = db.base.find(query,{"_id":0})
            depart_avg = db.depart_avg.find_one(query, {"_id": 0})
            total_data = list(people)
            bubble_data = map(form_bubble_data,total_data)
            total_person_data = total_data
        elif firstd == u'一级部门':  # 一级部门数据
            query = {"事业部": based}
            people = db.first_depart_avg.find(query, {"_id": 0})
            depart_avg = db.base_depart_avg.find_one(query,{"_id":0})
            total_data = list(people)
            total_person_data = list(db.base.find(query,{"_id":0}))
            bubble_data = form_department_bubble_data(total_person_data)
        elif secondd == u'二级部门':  # 二级部门数据
            query = {"事业部": based, "一级部门": firstd}
            people = db.depart_avg.find(query, {"_id": 0})
            depart_avg = db.first_depart_avg.find_one(query, {"_id": 0})
            total_data = list(people)
            total_person_data = list(db.base.find(query, {"_id": 0}))
            bubble_data = form_department_bubble_data(total_person_data)
        else:
            query = {"事业部": based, "一级部门": firstd, "二级部门": secondd}
            people = db.base.find(query, {"_id": 0})
            depart_avg = db.depart_avg.find_one(query, {"_id": 0})
            total_person_data = total_data = list(people)
            bubble_data = map(form_bubble_data,total_data)
        sum_data = form_total_data(total_person_data)
        print sum_data
        avg_score = [depart_avg[u'团队建设'], depart_avg[u'员工培养'], depart_avg[u'协调安排'], depart_avg[u'合理授权']]
        table1_head = [u'姓名', u'工作业绩得分', u'能力素质得分', u'价值观得分', u'绩效得分', u'绩效分类']
        table2_head = [u'姓名', u'团队建设', u'员工培养', u'协调安排', u'合理授权', u'能力素质得分']
        table3_head = [u'姓名', u'变革敏锐力', u'结果敏锐力', u'人际敏锐力', u'思维敏锐力']


        result = {'staff_data': map(self.map_data, total_data)}
        result.update({"table1_head": table1_head,
                       'table2_head': table2_head,
                       'table3_head': table3_head,
                       'avg_score': avg_score,
                       'bubble_data':bubble_data,
                       'total_data':sum_data,
                       'total_head':["S","A","B","C","D"]
                       })
        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps(result, ensure_ascii=False))


    def map_data(self, data):
        '''每个人的得分list
            如果没有姓名，则指定部门为姓名'''
        score = [data[u'团队建设'], data[u'员工培养'], data[u'协调安排'], data[u'合理授权']]
        data.update({"person_score": score})
        if not data.get(u'姓名'):
            data[u'姓名'] = data.get(u'二级部门') if data.get(u'二级部门') else data.get(u'一级部门')
        return data



class GetheadHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    # @tornado.web.authenticated
    def get(self):
        people = db.base.find_one({},{"_id" : 0})
        head = people.keys()
        result = {"unchosen_head":head}
        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps(result, ensure_ascii=False))



class GetselectorHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    # @tornado.web.authenticated
    def get(self):
        departments = db.department_info.find({},{"_id" : 0})
        res = {}
        current_user = self.current_user
        user = db.admin_user.find_one({"username":current_user})

        for i in departments:
            res[i.get('department')] = i.get('info')
        result = {'department_data':res, 'current_user':current_user}

        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps(result, ensure_ascii=False))






class UpLoadHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    # @tornado.web.authenticated
    def post(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        file = self.request.files['file'][0]
        print file.get('content_type')
        filename = file.get('filename')
        with open("{}/{}".format(base_path,filename),'w') as f:
            f.write(file.get('body'))
        f.close()
        self.set_header("Content-Type", "application/json")
        self.finish()



class GetWeiboAuthHandler(tornado.web.RequestHandler):
    # def set_default_headers(self):
    #     self.set_header("Access-Control-Allow-Origin", "*")
    #     self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    #     self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    # @tornado.web.authenticated
    def get(self):
        print self.request.headers
        print self.request
        code = self.get_argument('code',"")
        access_token = self.get_argument('access_token',"")
        if access_token:
            print access_token
        if code:
            print code
        self.finish()



class LoginHandler(tornado.web.RequestHandler):
    # def set_default_headers(self):
    #     self.set_header("Access-Control-Allow-Origin", "*")
    #     self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    #     self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        self.redirect('static/login.html')

    def post(self):
        user = self.get_argument('user', '')
        password = self.get_argument('password', '')
        print user
        print password
        if is_validate_user(user, password):
            self.set_secure_cookie('user', session.Session.new(user))
            print "here"
            return self.redirect("static/main.html")
        else:
            print "wrong"
            return self.redirect('static/login.html')



class LogoutHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    # @tornado.web.authenticated
    def get(self):
        user = self.current_user
        session.Session.rm(user)
        self.clear_all_cookies()
        self.finish()






application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/get_data", GetdataHandler),
    (r"/get_head", GetheadHandler),
    (r"/get_selector", GetselectorHandler),
    (r"/upload_file", UpLoadHandler),
    (r"/get_weibo_auth", GetWeiboAuthHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),

    ],**settings)

if __name__ == "__main__":
    parse_command_line()
    application.listen(8887)
    tornado.ioloop.IOLoop.instance().start()