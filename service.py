#coding:utf-8


def form_total_data(people):
    total_mark = {"S":{"number":0},"A":{"number":0},"B":{"number":0},"C":{"number":0},"D":{"number":0}}
    for person in people:
        value = person.get(u'绩效得分')
        if value >= 95:
            total_mark['S']['number'] += 1
        elif value >=85:
            total_mark['A']['number'] += 1
        elif value >=70:
            total_mark['B']['number'] += 1
        elif value >=60:
            total_mark['C']['number'] += 1
        else:
            total_mark['D']['number'] += 1
    total_num = len(people)
    for i in total_mark:
        total_mark[i]['persentage'] = '%.1f%%'%(total_mark[i]['number']*100/total_num)
    total_mark.update({"sum": total_num})
    return total_mark
