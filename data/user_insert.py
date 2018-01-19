#coding:utf-8

import xlrd
from hashlib import md5
from pymongo import MongoClient
import os
conn = MongoClient()
db = conn.hr
def md5_encrypt(data):
    m = md5()
    m.update(data)
    return m.hexdigest()

base_path = os.path.dirname(os.path.abspath(__file__))
path = '{}/../excel_doc/user_insert.xlsx'.format(base_path)
data = xlrd.open_workbook(path)
table = data.sheets()[0]
nrows = table.nrows
head = table.row_values(0)
for i in range(1,nrows):
    data = table.row_values(i)
    print data
    [username,passwd,base,first,second,is_admin] = data
    password = md5_encrypt(passwd)
    db.admin_user.insert(dict(username=username,
                              password=password,
                              base_level=base,
                              first_level=first,
                              second_level=second,
                              is_admin=is_admin))
