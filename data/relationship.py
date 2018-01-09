#coding:utf-8
import xlrd
import time
import pymysql
import datetime
import torndb
import time
import sys



reload(sys)
sys.setdefaultencoding('utf8')




db = torndb.Connection("127.0.0.1:3306", "hr", user="root", password="")
path = '/Users/zhangjack/Desktop/excel/test/Wechat考核关系导入.xlsx'
data = xlrd.open_workbook(path)
table = data.sheets()[-1]
titles = table.row_values(0)
def timestamp_to_time(timestamp):
    if len(str(timestamp)) > 10:
        timestamp = float(str(timestamp)[0:10])
    format_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
    return format_time



def create_tables():
    form = '{} varchar(40), '
    for i in titles:
        print i
        i = i.encode('utf-8')
        print form.format(i)

    enc_list = map(lambda i:i.encode('utf-8'),titles)

    la =  map(lambda i:form.format(i),enc_list)
    sql = ("create table relationship ("
           "`id` INT UNSIGNED AUTO_INCREMENT,"
           " {} PRIMARY KEY ( `id` ))"
           " ENGINE=InnoDB DEFAULT CHARSET=utf8;"
           )

    print sql.format("".join(la))
    # sql = CREATE TABLE IF NOT EXISTS `runoob_tbl`(
    #    `id` INT UNSIGNED AUTO_INCREMENT,
    #
    #    PRIMARY KEY ( `id` )
    # )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    createsql = '''create table relationship1 (`id` INT UNSIGNED AUTO_INCREMENT, 姓名 varchar(40), 所属公司 varchar(40), 一级部门 varchar(40), 二级部门 varchar(40), 职位名称 varchar(40), 直接主管 varchar(40), 同级1 varchar(40), 同级2 varchar(40), 跨部门同级3 varchar(40), 下级1 varchar(40), 下级2 varchar(40), 入职时间 varchar(40), 试用期截止时间 varchar(40), 评估表递交 varchar(40), 是否转正 varchar(40),  PRIMARY KEY ( `id` )) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
    insertsql='''insert into relationship ('姓名', '所属公司', '一级部门', '二级部门', '职位名称', '直接主管', '同级1', '同级2', '跨部门同级3', '下级1', '下级2', '入职时间')  values  (u'\u53f6\u6ee8', u'\u5c0f\u53f6\u5b50', u'\u516c\u53f8\u9886\u5bfc', u'\u516c\u53f8\u9886\u5bfc', u'CEO', u'', u'', u'', u'', u'', u'', '2013-04-01 00:00:00')
'''
nrows = table.nrows
for i in range(nrows-1):
    date = table.row_values(i+1)[-1]
    timestp = (date-70*365-19)*86400-8*3600
    values = table.row_values(i+1)[:-1]
    values.append(timestamp_to_time(timestp).split(' ')[0])
    values = map(lambda a: a if a else None, values)
    sql = "insert into relationship (name,company,department_1,department_2,title,master,colleage_1,colleage_2,cross_colleage_3,worker_1,worker_2,company_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    print sql
    db.execute(sql,*values)
# date = table.row_values(1)[-1]
# timestp = (date-70*365-19)*86400-8*3600
# enc_list = map(lambda i: i.encode('utf-8'), titles)
# tl = []
#
# values = table.row_values(1)[:-1]
# values.append(timestamp_to_time(timestp).split(' ')[0])
# values = map(lambda a:a if a else None, values)
#
# # value_sql = ",".join(values)
# print value_sql
# print str(tuple(values)).decode('string_escape')
# sql = "insert into relationship (name,company,department_1,department_2,title,master,colleage_1,colleage_2,cross_colleage_3,worker_1,worker_2,company_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
# print sql
# db.execute(sql,*values)








