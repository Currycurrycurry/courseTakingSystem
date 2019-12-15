import json
import traceback
from django.http import JsonResponse

from selectCourse.logs import logger
from selectCourse.util import sql_util
from django.db import connection
from selectCourse.constants.errorConstants import *
from selectCourse.constants.infoConstants import *
from selectCourse.service.base_service import BaseService

class CheckService(BaseService):
    def __init__(self, request):
        super(CheckService, self).__init__(request)
        if request.method == 'POST':
            self.data = request.POST

    def checkCourseTable(self):
        if self.request.session['is_login'] != True or self.request.session['role'] != STUDENT_ROLE:
            self._init_response()
            return self._get_response(UNAUTHORIZED_AS_STUDENT)

        try:
            user_id = self.data['user_id']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)
        
        try:
            cursor = connection.cursor()
            check_courses_sql = 'select * from section natural join course natural join teaches natural join takes natural join instructor where student_id = %s'
            cursor.execute(check_courses_sql,(user_id,))
            
            raw_courses_taken = sql_util.dictfetchall(cursor)
            print("raw courses taken are :",raw_courses_taken)
            total_num = len(raw_courses_taken)
            print("total num is ",total_num)
            sections = []
            for row in raw_courses_taken:
                tmp = {
                    'title':row['title'],
                    'course_id':row['course_id'],
                    'section_id':row['section_id'],
                    'dept_name':row['dept_name'],
                    'instructor_name':row['instructor_name'],
                    'credits':row['credits'],
                    'classroom_no':row['classroom_no'],
                    'day':row['day'],
                    'time':row['time'],
                    'lesson':row['lesson'],    
                }
                
                sections.append(tmp)
            res = {
                'total_num':total_num,
                'sections':sections,
            }
           
            self.response.update(res)
            self._init_response()
            return self._get_response(SHOW_COURSE_TABLE,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

    def checkStudentInfo(self,user_id):
        try:
            cursor = connection.cursor()
            check_personal_info_sql = "SELECT * FROM 'student' where 'student'.'student_id'='"+user_id+"'"
            cursor.execute(check_personal_info_sql)
            student_info = sql_util.dictfetchone(cursor)
            
            sql = 'select * from takes natural join course where student_id = %s'
            cursor.execute(sql,(user_id,))
            take_infos = sql_util.dictfetchall(cursor)
            gpa = 0
            grade_dict = {}
            total_credit = 0
            for take_info in take_infos:
                title = take_info['title']
                grade = take_info['grade']
                credits = take_info['credits']
                if grade != None:
                    grade_dict[title] = grade
                else:
                    grade_dict[title] = "无"

                total_credit+=credits
                for item in GRADE_DICT:
                    if grade == item:
                        gpa += GRADE_DICT[grade] * credits
                        break
            if total_credit != 0:
                gpa = float(gpa/total_credit)          

            res = {"grade_list":grade_dict,
                    "gpa":gpa}
            self._init_response()
            self.response.update(student_info)
            self.response.update(res)
            return self._get_response(SHOW_PERSONAL_INFO)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

    def checkInstructorInfo(self,user_id):
        try:
            cursor = connection.cursor()
            check_personal_info_sql = "SELECT * FROM 'instructor' where 'instructor'.'instructor_id'='"+user_id+"'"
            cursor.execute(check_personal_info_sql)
            instructor_info = sql_util.dictfetchone(cursor)

            self._init_response()
            self.response.update(instructor_info)
            return self._get_response(SHOW_PERSONAL_INFO)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

    def checkPersonalInfo(self):
        if self.request.session['is_login'] != True:
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            user_id = self.data['user_id']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)
        

        if self.request.session['role'] == STUDENT_ROLE:
            return self.checkStudentInfo(user_id)
        
        elif self.request.session['role'] == INSTRUCTOR_ROLE:
            return self.checkInstructorInfo(user_id)
        else:
            self._init_response()
            return self._get_response(UNAUTHORIZED)

    # TODO wait for more tests
    # TODO ljx the exam table 不完整？
    def checkExamTable(self):
        if self.request.session['is_login'] != True or self.request.session['role'] != STUDENT_ROLE:
            self._init_response()
            return self._get_response(UNAUTHORIZED_AS_STUDENT)

        try:
            user_id = self.data['user_id']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)
        
        try:
            cursor = connection.cursor()
            # check_exams_sql = "select * from (SELECT * FROM (SELECT * FROM 'section' NATURAL JOIN 'takes' WHERE 'takes'.'student_id'='"+user_id+"') NATURAL JOIN 'course') natural join exam "
            # cursor.execute(check_exams_sql)
            sql = 'select * from section natural join takes natural join course natural join exam where student_id = %s'
            cursor.execute(sql,(user_id,))
            raw_exams_taken = sql_util.dictfetchall(cursor)
            print("raw courses taken are :",raw_exams_taken)
            total_num = len(raw_exams_taken)
            print("total num is ",total_num)
            # sections = list(raw_courses_taken)
            sections = []
            for row in raw_exams_taken:
                tmp = {
                    'title':row['title'],
                    'course_id':row['course_id'],
                    'section_id':row['section_id'],
                    'classroom_no':row['classroom_no'],
                    'day':row['day'],
                    'start_time':row['start_time'],
                    'end_time':row['end_time'],
                    'open_note_flag':row['open_note_flag'],  
                    'type':row['type']  
                }
                sections.append(tmp)

            res = {
                'total_num':total_num,
                'exams':sections,
            }
           
            self.response.update(res)
            self._init_response()
            return self._get_response(SHOW_EXAM_TABLE,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)





        pass

    def checkTaughtCourses(self):
        if self.request.session['is_login'] != True or self.request.session['role'] != INSTRUCTOR_ROLE:
            self._init_response()
            return self._get_response(UNAUTHORIZED_AS_INSTRUCTOR)

        try:
            user_id = self.data['user_id']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)
        
        try:
            cursor = connection.cursor()
            check_courses_taught_sql ="SELECT * FROM (SELECT * FROM 'teaches' NATURAL JOIN 'section' WHERE 'teaches'.'instructor_id' = '"+user_id+"') NATURAL JOIN 'course' "
            cursor.execute(check_courses_taught_sql)
            raw_courses_taught = sql_util.dictfetchall(cursor)
            print("raw courses taught are :",raw_courses_taught)
            total_num = len(raw_courses_taught)
            print("total num is ",total_num)
            # sections = list(raw_courses_taken)
            sections = []
            for row in raw_courses_taught:
                tmp = {
                    'title':row['title'],
                    'course_id':row['course_id'],
                    'section_id':row['section_id'],
                    'dept_name':row['dept_name'],
                    'credits':row['credits'],
                    'classroom_no':row['classroom_no'],
                    'day':row['day'],
                    'time':row['time'],
                    'lesson':row['lesson'],    
                }
                sections.append(tmp)

            res = {
                'total_num':total_num,
                'sections':sections,
            }
           
            self.response.update(res)
            self._init_response()
            return self._get_response(SHOW_COURSE_TABLE,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)


    def checkCourseNameList(self):
        if self.request.session['is_login'] != True or self.request.session['role'] != INSTRUCTOR_ROLE:
            self._init_response()
            return self._get_response(UNAUTHORIZED_AS_INSTRUCTOR)

        try:
            user_id = self.data['user_id']
            course_id = self.data['course_id']
            section_id = self.data['section_id']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)
        
        try:
            cursor = connection.cursor()
            check_namelist_sql = "SELECT * FROM 'takes' NATURAL JOIN 'student' WHERE 'takes'.'course_id'='"+course_id+"' AND 'takes'.'section_id'="+section_id
            cursor.execute(check_namelist_sql)
            raw_namelist = sql_util.dictfetchall(cursor)
            print("raw name list taken are :",raw_namelist)
            total_num = len(raw_namelist)
            print("total num is ",total_num)
            sections = []
            for row in raw_namelist:
                tmp = {
                    'title':row['title'],
                    'student_id':row['course_id'],
                    'student_name':row['student_name'],
                    'student_major':row["student_major"],
                    'student_dept_name':row["student_dept_name"],
                    'grade':row['grade'],
                }
                sections.append(tmp)

            res = {
                'total_num':total_num,
                'sections':sections,
            }
           
            self.response.update(res)
            self._init_response()
            return self._get_response(SHOW_COURSE_TABLE,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)
        pass


    def execute(self):
        pass


