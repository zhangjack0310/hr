#coding:utf-8
__author__ = 'laobzhang'
import xlrd
import time

import datetime

import time
import sys
from pymongo import MongoClient
conn = MongoClient()
db = conn.hr
path = '/Users/zhangjack/Desktop/data_insert.xlsx'
data = xlrd.open_workbook(path)
table = data.sheets()[0]
pure_table = data.sheets()[1]
nrows = pure_table.nrows
head = table.row_values(0)
def base_data_insert():
    for i in range(nrows):
        data = pure_table.row_values(i)
        print data
        dic = {}
        for i in range(len(head)):
            dic.update({head[i]:data[i]})
        print dic
        dic[u'绩效得分'] = round(dic[u'绩效得分'],1)
        db.base.insert(dic)

def department_data():
    '''部门结构（含员工）'''
    base_department = pure_table.col_values(1)
    depart_list = list(set(base_department))
    depart_dic = {department:{} for department in depart_list}
    for i in range(nrows-1):
        # print pure_table.row_values(i)
        [name,based,firstd,secondd] = pure_table.row_values(i)[0:4]
        # print based,firstd,secondd
        if depart_dic[based].has_key(firstd):
            if depart_dic[based][firstd].has_key(secondd):
                depart_dic[based][firstd][secondd].append(name)
            else:
                depart_dic[based][firstd][secondd] = []
                depart_dic[based][firstd][secondd].append(name)

        else:
            depart_dic[based][firstd] = {}
    # print depart_dic
    for i in depart_dic:
        db.base_department.insert({"info":depart_dic[i],'department':i})


def department():
    '''部门结构'''
    datas = db.base_department.find()
    for data in datas:
        department_name = data.get('department')
        info = data.get('info')
        for first_department in info.keys():
            print first_department, info[first_department]
            print info[first_department].keys()
            for second_department in info[first_department].keys():
                print department_name,first_department,second_department
                db.department.insert(dict(department_name=department_name, first_department=first_department, second_department=second_department))





if __name__ == '__main__':
    # base_data_insert()
    # department_data()
    # department()
