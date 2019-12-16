import json
import traceback
from django.http import JsonResponse

from selectCourse.logs import logger
from selectCourse.util import sql_util
from django.db import connection
from selectCourse.constants.errorConstants import *
from selectCourse.constants.infoConstants import *
from selectCourse.service.base_service import BaseService



# TODO test the no_vacancy section_time_conflict conditions!
class SelectService(BaseService):
    def __init__(self, request):
        super(SelectService, self).__init__(request)
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

            if raw_take_info != None:
                self._init_response()
                return self._get_response(ALREADY_SELECT,-1)

            find_take_num_sql = "SELECT COUNT(*) FROM 'takes' WHERE 'takes'.'course_id' = '"+course_id+"' AND 'takes'.'section_id' ="+section_id
            cursor.execute(find_take_num_sql)
            raw_take_num =cursor.fetchone()
            print("the take num is :",raw_take_num[0])
            find_section_limit = "SELECT 'section'.'limit' FROM 'section' WHERE 'section'.'course_id'='"+course_id+"' AND 'section'.'section_id' ="+section_id
            cursor.execute(find_section_limit)
            raw_section_limit =sql_util.dictfetchone(cursor)
            print("the section limit is :",raw_section_limit['limit'])

            if raw_section_limit['limit'] <= raw_take_num[0]:
                self._init_response()
                return self._get_response(NO_VACANCY,-1)

            # section time conflict

            section_day = int(raw_section_info['day'])
            section_time = raw_section_info['time']
            section_start_time = int(section_time.split("-")[0])
            section_end_time = int(section_time.split("-")[1])

            find_takes_sql = 'select * from takes where course_id = %s and section_id = %s and student_id = %s'
            cursor.execute(find_takes_sql,(course_id,section_id,user_id,))
            takes_info = sql_util.dictfetchall(cursor)
            
            for item in takes_info:
                tmp_day = int(item['day'])
                tmp_time = item['time']
                tmp_start_time = int(tmp_time.split("-")[0])
                tmp_end_time = int(tmp_time.split("-")[1])
                if tmp_day == section_day:
                    if (section_start_time >= tmp_start_time and section_start_time <= tmp_end_time) or \
                        (section_start_time <= tmp_start_time and section_start_time >= tmp_end_time):
                        self._init_response()
                        return self._get_response(SECTION_TIME_CONFLICT)
            
            # application conflict
            app_sql = 'select * from application where course_id=%s and section_id=%s and student_id=%s and if_drop=1'
            cursor.execute(app_sql,(course_id,section_id,user_id))
            raw_app = sql_util.dictfetchall(cursor)
            if raw_app != None:
                self._init_response()
                return self._get_response(DROP_SELECT_ERROR)

            insert_takes_sql = "INSERT INTO 'takes' ('course_id','section_id','student_id','grade','drop_flag') SELECT '"+ course_id+"',"+section_id+",'"+user_id+"', NULL,0"
            cursor.execute(insert_takes_sql)
            check_credit_sql = "SELECT 'student'.'student_total_credit' FROM 'student' WHERE 'student'.'student_id' = '"+user_id+"'"
            cursor.execute(check_credit_sql)
            raw_credit = sql_util.dictfetchone(cursor)
            credit_before = raw_credit['student_total_credit']
            print("before update: the raw_credit is : ",credit_before)

            find_course_credit_sql = "SELECT 'course'.'credits' FROM 'course' WHERE 'course'.'course_id'='"+course_id+"'"
            cursor.execute(find_course_credit_sql)
            raw_course_credit = sql_util.dictfetchone(cursor)
            course_credit = raw_course_credit['credits']
            print("the course credit is ",course_credit)
            updated_credit = int(credit_before+course_credit)
            print("updated credit is",updated_credit)
            add_credits_sql = "UPDATE 'student' SET 'student_total_credit'="+str(updated_credit)+" WHERE 'student'.'student_id'='"+user_id+"'"
            cursor.execute(add_credits_sql)

            self._init_response()
            return self._get_response(SELECT_OK,1)
                            
        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)
            




