# coding=utf-8
import json
import re
import os
os.sys.path.append('..')

# '657935': {'cid': '657935', 'num': 'SOFT130012.01', 'name': '计算机前沿讲座(下)', 'credit': '0', 'tutor': '赵一鸣', 'title': '正高级讲师', 'limit': '130', 'place': ' \r\n', 'timing': '\t\t\t\t星期五 6-7 [1-16]  \r\n', 'depart': '软件学院'}
from selectCourse.models import *


def getDayStr(line):
    day_p = re.compile(r'[^\u4e00-\u9fa5]') 
    reses = day_p.split(line)
    for res in reses:
        if res!='':
            return res
    return "未知"

def getTimeNums(line):
    return re.findall(r'[0-9]+',line)


# print(getWeekNums('\t\t\t\t星期五 6-7 [1-16]  \r\n'))
fd = open('./courses.json','r')
data = json.load(fd)
# print(data)
# print(len([ci for ci in data.values() if len(ci['num']) > 5]))

for course_item in data.values():
    # TODO for later to modify 
    id = course_item['num']
    if len(id)>4:
        print(id)
        Course.objects.get_or_create(course_id=course_item['cid'],title=course_item['name'],credit=course_item['credit'],course_dept_name=course_item['depart'])
        Classroom.objects.get_or_create(classroom_no = course_item['place']) 
        unprocessed_time = course_item['timing'] # like '\t\t\t\t星期五 6-7 [1-16]  \r\n'
        times = getTimeNums(unprocessed_time)
        Time_slot.objects.get_or_create(day=getDayStr(unprocessed_time),start_time=times[0],end_time=times[1],start_week=times[2],end_week=times[3])
        Section.objects.get_or_create(section_id=course_item['num'],limit=course_item['limit'])

        Instructor.objects.get_or_create()

        



        

