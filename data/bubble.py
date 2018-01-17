#coding:utf-8
from pymongo import MongoClient
conn = MongoClient()
db = conn.hr
people = db.base.find_one({"事业部":"总部","一级部门":"财务部","二级部门":"财务部"})
from bubble_option import datasets
def form_bubble_data(person):
    jixiao = person.get(u'绩效得分')
    qianli = person.get(u'潜力得分')
    if jixiao>85:
        if qianli>85:
            level = 1
        elif qianli>70:
            level = 2
        else:
            level = 4
    elif jixiao>70:
        if qianli>85:
            level = 3
        elif qianli>70:
            level = 5
        else:
            level = 6
    else:
        if qianli>85:
            level = 7
        elif qianli>70:
            level = 8
        else:
            level = 9
    return form_colour(person.get(u'姓名'), jixiao, qianli, level)

def form_colour(name,jixiao,qianli,level):
    if level == 1:
        data = {
        "backgroundColor": "rgba(255,165,0,0.4)",
        "borderColor": "rgba(255,165,0,1)",
        }
    elif level in [2,3]:
        data = {
            "backgroundColor": "rgba(72,209,204,0.4)",
            "borderColor": "rgba(72,209,204,1)",
        }
    elif level in [4,5,6]:
        data = {
            "backgroundColor": "rgba(135,206,235,0.4)",
            "borderColor": "rgba(135,206,235,1)",
        }
    elif level in [7,8]:
        data = {
            "backgroundColor": "rgba(255,127,80,0.4)",
            "borderColor": "rgba(255,127,80,1)",
        }
    elif level ==9:
        data = {
            "backgroundColor": "rgba(128,128,128,0.4)",
            "borderColor": "rgba(128,128,128,1)",
        }
    else:
        data = {}
    data.update({
            'label': name,
            "data": [{
                "x": jixiao,
                "y": qianli,
                "r": 15
            }]})
    return data

def form_department_bubble_data(people):
    bubble_data = datasets
    print id(bubble_data)
    dic = {}
    re_bubble = {}
    for person in people:
        jixiao = person.get(u'绩效得分')
        qianli = person.get(u'潜力得分')
        if jixiao > 85:
            if qianli > 85:
                level = '1'
            elif qianli > 70:
                level = '2'
            else:
                level = '4'
        elif jixiao > 70:
            if qianli > 85:
                level = '3'
            elif qianli > 70:
                level = '5'
            else:
                level = '6'
        else:
            if qianli > 85:
                level = '7'
            elif qianli > 70:
                level = '8'
            else:
                level = '9'
        if re_bubble.has_key(level):
            re_bubble[level]['data'][0]["r"] += 3.5
        else:
            bubble_data[level]['data'][0]["r"] = 0
            re_bubble[level] = bubble_data[level]
            re_bubble[level]['data'][0]["r"] += 3.5

        if dic.has_key(level):
            dic[level] += 1
        else:
            dic[level] = 1
    for i in dic:

        re_bubble[i]['label'] = u"Level:{} 人数:{}".format(i,dic[i])
    return re_bubble.values()


li = ['绩效分类','一级部门','工作业绩得分','价值观得分','绩效得分','团队建设','潜力得分','二级部门','合理授权','协调安排','潜力分类','姓名','事业部','能力素质得分','员工培养']