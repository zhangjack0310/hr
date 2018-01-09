#coding:utf-8

from pymongo import MongoClient
import sys
print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

print sys.getdefaultencoding()
conn = MongoClient()
db = conn.hr
def get_avg(first=True,second=True):
    group_id = {"事业部":"$事业部"}
    project = {"事业部":"$_id.事业部","_id":0, "团队建设":1, "员工培养":1, "协调安排":1, "合理授权":1}
    if first:
        group_id.update({"一级部门":"$一级部门"})
        project.update({"一级部门":"$_id.一级部门"})
    if second:
        group_id.update({"二级部门":"$二级部门"})
        project.update({"二级部门":"$_id.二级部门"})

    data = db.base.aggregate([
        {"$group":{"_id":group_id,
                   "团队建设": {"$avg": "$团队建设"},
                   "员工培养": {"$avg": "$员工培养"},
                   "协调安排": {"$avg": "$协调安排"},
                   "合理授权": {"$avg": "$合理授权"},
                   }},
        {"$project":project}
    ]).get('result')
    for dic in data:
        print dic

        round_list = [u'团队建设', u'员工培养', u'协调安排', u'合理授权']
        for i in round_list:
            dic[i] = round(dic[i],1)
        db.depart_avg.insert(dic)






if __name__ == '__main__':
    # get_avg()
