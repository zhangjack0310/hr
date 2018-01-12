#coding:utf-8
__author__ = 'laobzhang'
import xlrd
import time
import sys
print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

import datetime
import os
import time
import sys
from pymongo import MongoClient
conn = MongoClient()
db = conn.hr
base_path = os.path.dirname(os.path.abspath(__file__))
path = '{}/../data_insert.xlsx'.format(base_path)
data = xlrd.open_workbook(path)
table = data.sheets()[0]
nrows = table.nrows
head = table.row_values(0)
def base_data_insert():
    for i in range(1,nrows):
        data = table.row_values(i)
        print data
        dic = {}
        for i in range(len(head)):
            dic.update({head[i]:data[i]})
        print dic
        dic[u'绩效得分'] = round(dic[u'绩效得分'],1)
        db.base.insert(dic)

def department_data():
    '''部门结构（含员工）'''
    base_department = table.col_values(1)[1:]
    depart_list = list(set(base_department))
    depart_dic = {department:{} for department in depart_list}
    for i in range(1,nrows):
        # print pure_table.row_values(i)
        [name,based,firstd,secondd] = table.row_values(i)[0:4]
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

def department_pure_data():
    '''部门结构（不含员工）'''
    base_department = table.col_values(1)[1:]
    depart_list = list(set(base_department))
    depart_dic = {department:{} for department in depart_list}
    for i in range(1,nrows):
        # print pure_table.row_values(i)
        [name,based,firstd,secondd] = table.row_values(i)[0:4]
        # print based,firstd,secondd
        if depart_dic[based].has_key(firstd):
            depart_dic[based][firstd].append(secondd)
        else:
            depart_dic[based][firstd] = []
    # print depart_dic
    for based in depart_dic:
        for firstd in depart_dic[based]:
            depart_dic[based][firstd] = list(set(depart_dic[based][firstd]))
    for i in depart_dic:
        db.department_info.insert({"info":depart_dic[i],'department':i})



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


li = ['绩效分类','一级部门','工作业绩得分','价值观得分',
      '绩效得分','团队建设','潜力得分','二级部门',
      '合理授权','协调安排','潜力分类','姓名',
      '事业部','能力素质得分','员工培养']
avg_item = [u'工作业绩得分',u'价值观得分',u'绩效得分',u'团队建设',u'潜力得分',u'合理授权',u'协调安排',u'能力素质得分',u'员工培养', u'变革敏锐力', u'结果敏锐力', u'人际敏锐力', u'思维敏锐力']
# print {i:{"$avg":"${}".format(i)} for i in avg_item}

def get_avg(first=True,second=True):
    group_id = {"事业部":"$事业部"}
    project = {"事业部":"$_id.事业部","_id":0}
    project.update({i: 1 for i in avg_item})
    if first:
        group_id.update({"一级部门":"$一级部门"})
        project.update({"一级部门":"$_id.一级部门"})
    if second:
        group_id.update({"二级部门":"$二级部门"})
        project.update({"二级部门":"$_id.二级部门"})
    group_data = {"_id":group_id}
    group_data.update({i:{"$avg":"${}".format(i)} for i in avg_item})

    data = db.base.aggregate([
        {"$group": group_data},
        {"$project":project}
    ]).get('result')
    for dic in data:

        round_list = avg_item
        for i in round_list:
            dic[i] = round(dic[i],1)
        print dic
        if second:
            db.depart_avg.insert(dic)
        elif first:
            db.first_depart_avg.insert(dic)
        else:
            db.base_depart_avg.insert(dic)






if __name__ == '__main__':
    base_data_insert()
    department_data()
    department()
    department_pure_data()
    get_avg()
    get_avg(second=False)
    get_avg(first=False,second=False)
