#coding:utf-8
import xlrd
import time
import pymysql
import datetime
import torndb
import time
import sys
db = torndb.Connection("127.0.0.1:3306", "hr", user="root", password="")
path = '/Users/zhangjack/Desktop/excel/master1.xlsx'
data = xlrd.open_workbook(path)
table = data.sheets()[-1]
nrows = table.nrows
print nrows
def insert_manage(data):
    sql = "insert into manage_table (name,master,colleage_1,colleage_2,staff) values (%s,%s,%s,%s,%s)"
    db.execute(sql, *data)

def insert_staff(data):
    sql = "insert into staff_table (name,master,colleage_1,colleage_2,colleage_cross) values (%s,%s,%s,%s,%s)"
    db.execute(sql, *data)

def manage_table():
    for i in range(nrows):
        data = table.row_values(i)
        print data
        insert_staff(data)



manage_table()
