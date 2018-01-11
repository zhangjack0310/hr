#coding:utf-8

from pymongo import MongoClient
import sys
print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

print sys.getdefaultencoding()
conn = MongoClient()
db = conn.hr
li = ['绩效分类','一级部门','工作业绩得分','价值观得分',
      '绩效得分','团队建设','潜力得分','二级部门',
      '合理授权','协调安排','潜力分类','姓名',
      '事业部','能力素质得分','员工培养']
avg_item = [u'工作业绩得分',u'价值观得分',u'绩效得分',u'团队建设',u'潜力得分',u'合理授权',u'协调安排',u'能力素质得分',u'员工培养']
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
    # pass
    get_avg()
    get_avg(second=False)
    get_avg(first=False,second=False)
