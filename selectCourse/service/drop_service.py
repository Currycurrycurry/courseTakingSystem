import json
import traceback
from django.http import JsonResponse

from selectCourse.logs import logger
from selectCourse.util import sql_util
from django.db import connection
from selectCourse.constants.errorConstants import *
from selectCourse.constants.infoConstants import *
from selectCourse.service.base_service import BaseService


class DropService(BaseService):
    def __init__(self, request):
        super(DropService, self).__init__(request)
        if request.method == 'POST':
            self.data = request.POST

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



