#coding:utf-8
from hashlib import md5
from pymongo import MongoClient
conn = MongoClient()
db = conn.hr
def md5_encrypt(data):
    m = md5()
    m.update(data)
    return m.hexdigest()


def form_total_data(people):
    total_mark = {"S":{"number":0},"A":{"number":0},"B":{"number":0},"C":{"number":0},"D":{"number":0}}
    for person in people:
        value = person.get(u'绩效分类')
        if value == "S":
            total_mark['S']['number'] += 1
        elif value =="A":
            total_mark['A']['number'] += 1
        elif value =="B":
            total_mark['B']['number'] += 1
        elif value =="C":
            total_mark['C']['number'] += 1
        else:
            total_mark['D']['number'] += 1
    total_num = len(people)
    for i in total_mark:
        total_mark[i]['persentage'] = '%.1f%%'%(total_mark[i]['number']*100/total_num)
    total_mark.update({"sum": total_num})
    return total_mark

def is_validate_user(user,password):
    passwd = md5_encrypt(password)
    user_info = db.admin_user.find_one({"username": user})
    if not user_info:
        return False
    elif passwd != user_info.get('password'):
        return False
    else:
        return True