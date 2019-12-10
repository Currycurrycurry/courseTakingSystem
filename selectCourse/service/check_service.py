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

    # TODO add the exam info into the courseTable
    # TODO add the instructor info into the courseTable 
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
            check_courses_sql = "SELECT * FROM (SELECT * FROM 'section' NATURAL JOIN 'takes' WHERE 'takes'.'student_id'='"+user_id+"') NATURAL JOIN 'course' "
            cursor.execute(check_courses_sql)
            raw_courses_taken = sql_util.dictfetchall(cursor)
            print("raw courses taken are :",raw_courses_taken)
            total_num = len(raw_courses_taken)
            print("total num is ",total_num)
            # sections = list(raw_courses_taken)
            sections = []
            for row in raw_courses_taken:
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

    def checkAllCourses(self):

        if self.request.session['is_login'] != True or \
            (self.request.session['role'] != STUDENT_ROLE and self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)
        
        try:
            page_num = int(self.data['current_page_num']) #0,1,2,...
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        
        try:
            cursor = connection.cursor()

            check_all_courses_sql = "SELECT * FROM 'section' NATURAL JOIN 'course' limit %s,%s"
            cursor.execute(check_all_courses_sql,(page_num*ITEM_NUM_FOR_ONE_PAGE),ITEM_NUM_FOR_ONE_PAGE,)
            raw_courses = sql_util.dictfetchall(cursor)
            print("raw courses are :",raw_courses)
            total_num_sql = 'select count(*) from section'
            cursor.execute(total_num_sql)
            total_num = int(cursor.fetchone()[0])
            print("total num is ",total_num)
            # sections = list(raw_courses_taken)
            sections = []
            for row in raw_courses:
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
            return self._get_response(SHOW_COURSES,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

    # TODO calculate gpa and show grade of every courses taken
    def checkStudentInfo(self,user_id):
        try:
            cursor = connection.cursor()
            check_personal_info_sql = "SELECT * FROM 'student' where 'student'.'student_id'='"+user_id+"'"
            cursor.execute(check_personal_info_sql)
            student_info = sql_util.dictfetchone(cursor)
            
            self._init_response()
            self.response.update(student_info)
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

    # TODO check the instructor info
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
            check_exams_sql = "select * from (SELECT * FROM (SELECT * FROM 'section' NATURAL JOIN 'takes' WHERE 'takes'.'student_id'='"+user_id+"') NATURAL JOIN 'course') natural join exam "
            cursor.execute(check_exams_sql)
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
                'sections':sections,
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

    # TODO wait for more tests
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
        if self.request.session['is_login'] != True or self.request.session['role'] != STUDENT_ROLE:
            self._init_response()
            return self._get_response(UNAUTHORIZED_AS_STUDENT)

        try:
            user_id = self.data['user_id']
            course_id = self.data['course_id']
            section_id = self.data['section_id']
            print("the course id is ",course_id)
            print("the section id is ",section_id)

        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()
            find_course_sql = "SELECT 'course'.'course_id' FROM 'course' WHERE 'course'.'course_id' ='"+course_id+"'"
            cursor.execute(find_course_sql)
            raw_course_id = sql_util.dictfetchone(cursor)
            print("raw course id is ",raw_course_id)

            if raw_course_id == None:
                self._init_response()
                return self._get_response(WRONG_COURSE_ID,-1)


            find_section_sql = "SELECT * FROM 'section' WHERE 'section'.'course_id' ='"+course_id+"' AND 'section'.'section_id'="+section_id
            cursor.execute(find_section_sql)
            raw_section_info =sql_util.dictfetchone(cursor)

            if raw_section_info == None:
                self._init_response()
                return self._get_response(WRONG_SECTION_ID,-1)

            find_whether_already_takes_sql = "SELECT * FROM 'takes' WHERE 'takes'.'course_id' = '"+course_id+"' AND 'takes'.'section_id' ="+section_id+" AND 'takes'.'student_id'='"+user_id+"'"
            cursor.execute(find_whether_already_takes_sql)
            raw_take_info =sql_util.dictfetchone(cursor)
            print("raw take info is ",raw_take_info)

            if raw_take_info == None:
                self._init_response()
                return self._get_response(NOT_TAKE,-1)

            drop_course_sql = "DELETE FROM 'takes' WHERE ('takes'.'course_id' = '"+course_id+"' AND 'takes'.'section_id' ="+section_id+" AND 'takes'.'student_id' = '"+user_id+"')"
            cursor.execute(drop_course_sql)

            check_credit_sql = "SELECT 'student'.'student_total_credit' FROM 'student' WHERE 'student'.'student_id' = '"+user_id+"'"
            cursor.execute(check_credit_sql)
            raw_credit = cursor.fetchone()
            print("before update: the raw_credit is : ",raw_credit[0])
            find_course_credit_sql = "SELECT 'course'.'credits' FROM 'course' WHERE 'course'.'course_id'='"+course_id+"'"
            cursor.execute(find_course_credit_sql)
            raw_course_credit = cursor.fetchone()
            print("the course credit is ",raw_course_credit[0])
            updated_credit = int(raw_credit[0]-raw_course_credit[0])
            print("updated credit is",updated_credit)
            minus_credits_sql = "UPDATE 'student' SET 'student_total_credit'="+str(updated_credit)+" WHERE 'student'.'student_id'='"+user_id+"'"
            cursor.execute(minus_credits_sql)

            self._init_response()
            return self._get_response(DROP_OK,1)
                        
        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)



