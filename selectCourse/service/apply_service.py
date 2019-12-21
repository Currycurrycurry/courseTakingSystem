import json
import traceback
from selectCourse.util import sql_util
from django.db import connection
from selectCourse.constants.errorConstants import *
from selectCourse.constants.infoConstants import *
from selectCourse.service.base_service import BaseService

class ApplyService(BaseService):
    def __init__(self, request):
        super(ApplyService, self).__init__(request)
        if request.method == 'POST':
            self.data = request.POST
        elif request.method == 'GET':
            self.data = request.GET

    def checkApplications(self):
        if self.request.session['is_login'] != True:
            self._init_response()
            return self._get_response(UNAUTHORIZED)


        try:
            user_id = self.data['user_id']
        except Exception as error:
            self._init_response()
            return self._get_response(GET_ARG_ERROR,-1)

        if self.request.session['role'] == STUDENT_ROLE:
            return self.checkApplicationsByStudent(user_id)
        
        elif self.request.session['role'] == INSTRUCTOR_ROLE:
            return self.checkApplicationsByInstructor(user_id)
        else:
            self._init_response()
            return self._get_response(UNAUTHORIZED)
    
    def checkApplicationsByStudent(self,user_id):
        try:
            cursor = connection.cursor()
            check_app_sql = 'select * from application natural join course natural join teaches natural join instructor where student_id = %s'
            cursor.execute(check_app_sql,(user_id,))
            app_infos = sql_util.dictfetchall(cursor)
            total_num = len(app_infos)
            app_infos = list(app_infos)
            res = {
                "total_num":total_num,
                "applications":app_infos
            }
                
            self._init_response()
            self.response.update(res)
            return self._get_response(SHOW_APPS,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)

    def checkApplicationsByInstructor(self,user_id):
        try:
            cursor = connection.cursor()
            sql = 'select * from teaches natural join application natural join course where instructor_id = %s'
            cursor.execute(sql,(user_id,))
            rows = sql_util.dictfetchall(cursor)
            total_num = len(rows)
            self._init_response()
            res = {
                'total_num':total_num,
                'applications':rows
            }
            self.response.update(res)
            return self._get_response(SHOW_APPS,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)

    def handleApplication(self):

        if self.request.session['is_login'] != True or (self.request.session['role'] != INSTRUCTOR_ROLE and self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED_AS_INSTRUCTOR)

        try:
            # user_id = self.data['user_id']
            student_id = self.data['student_id']
            course_id = self.data['course_id']
            section_id = self.data['section_id']
            status = self.data['status']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)
        
        try:
            cursor = connection.cursor()
            sql ="update application set status = " + status + " where course_id = '" +  course_id + "' and section_id = '" + section_id + "' and student_id = '" + student_id+"'"
            print(sql)
            cursor.execute(sql)
            if int(status) == 1:
                sql = 'insert into takes(course_id,section_id,student_id) '\
                    'values(%s,%s,%s)'
                cursor.execute(sql,(course_id,section_id,student_id))

            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)

    def submitApplication(self):

        if self.request.session['is_login'] != True or self.request.session['role'] != STUDENT_ROLE:
            self._init_response()
            return self._get_response(UNAUTHORIZED_AS_STUDENT)

        try:
            user_id = self.data['user_id']
            course_id = self.data['course_id']
            section_id = self.data['section_id']
            app_reason = self.data['application_reason']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)
        
        try:
            cursor = connection.cursor()
            sql = 'select * from application where course_id = %s and section_id = %s and student_id = %s'
            cursor.execute(sql,(course_id,section_id,user_id,))
            row = sql_util.dictfetchone(cursor)

            if row != None and int(row['if_drop']) == 1:
                self._init_response()
                return self._get_response(APP_DROPPED, -1)


            if row != None:
                self._init_response()
                return self._get_response(APP_ALREADY,-1)


            sql = 'select * from takes where course_id = %s and section_id = %s and student_id = %s'
            cursor.execute(sql,(course_id,section_id,user_id,))
            row = sql_util.dictfetchone(cursor)
            if row != None:
                self._init_response()
                return self._get_response(APP_SELECTED,-1)
            
            find_take_num_sql = "SELECT COUNT(*) FROM 'takes' WHERE 'takes'.'course_id' = '"+course_id+"' AND 'takes'.'section_id' ="+section_id
            cursor.execute(find_take_num_sql)
            raw_take_num = cursor.fetchone()
            print("the take num is :",raw_take_num[0])
            find_section_limit = "SELECT 'section'.'limit' FROM 'section' WHERE 'section'.'course_id'='"+course_id+"' AND 'section'.'section_id' ="+section_id
            cursor.execute(find_section_limit)
            raw_section_limit = cursor.fetchone()
            if raw_section_limit == None:
                self._init_response()
                return self._get_response("nonexist section ",-1)
            print("the section limit is :",raw_section_limit[0])


            find_section_capacity = "SELECT capacity FROM classroom NATURAL JOIN section WHERE course_id='"+course_id+"' AND section_id='"+section_id+"'"
            cursor.execute(find_section_capacity)
            raw_section_capacity = cursor.fetchone()
            print("the section capacity is ",raw_section_capacity[0])
            
            if raw_section_limit[0] > raw_take_num[0]:
                self._init_response()
                return self._get_response(APP_VACANCY,-1)
            elif raw_take_num[0] >= raw_section_capacity[0] :
                self._init_response()
                return self._get_response(APP_CAPACITY,-1)

            # section time conflict

            sql = 'select * from section where course_id=%s and section_id=%s'
            cursor.execute(sql,(course_id,section_id,))
            raw_section_info = sql_util.dictfetchone(cursor)

            section_day = int(raw_section_info['day'])
            section_start_time = int(raw_section_info['start'])
            section_end_time = int(raw_section_info['end'])

            find_takes_sql = "select * from takes natural join section where student_id = '" + user_id  + "'"
            print(find_takes_sql)
            cursor.execute(find_takes_sql)
            takes_info = sql_util.dictfetchall(cursor)
            print(takes_info)
            for item in takes_info:
                tmp_day = int(item['day'])
                tmp_start_time = int(raw_section_info['start'])
                tmp_end_time = int(raw_section_info['end'])
                print(tmp_day,section_day)
                if tmp_day == section_day:
                    print(1)
                    if (section_start_time >= tmp_start_time and section_start_time <= tmp_end_time) or \
                        ( section_end_time >= tmp_start_time and section_end_time <= tmp_end_time):
                        self._init_response()
                        return self._get_response(SECTION_TIME_CONFLICT,-1)

            # exam time conflict 
            sql_exam = 'select * from exam where course_id=%s and section_id=%s'
            cursor.execute(sql_exam,(course_id,section_id,))
            target = sql_util.dictfetchone(cursor)
            print("target",target)
            if target != None:
                exam_type = int(target['type'])
                if exam_type == 0:
                    exam_day = int(target['exam_day'])
                    exam_start_time = int(target['start_time'].split(":")[0])*60 + int(target['start_time'].split(":")[1])
                    exam_end_time = int(target['end_time'].split(":")[0])*60 + int(target['end_time'].split(":")[1])

                    sql = 'select * from takes natural join exam where student_id =%s'
                    cursor.execute(sql,(user_id,))
                    rows = sql_util.dictfetchall(cursor)
                    print("exam :",rows)

                    for row in rows:
                        tmp_type = int(row['type'])
                        if tmp_type == 0:
                            tmp_day = int(row['exam_day'])
                            tmp_start_time =  int(row['start_time'].split(":")[0])*60 + int(row['start_time'].split(":")[1])
                            tmp_end_time = int(row['end_time'].split(":")[0])*60 + int(row['end_time'].split(":")[1])

                            if (exam_start_time >= tmp_start_time and exam_start_time <=tmp_end_time)\
                                or (exam_end_time >= tmp_start_time and exam_end_time <= tmp_end_time):
                                self._init_response()
                                return self._get_response(EXAM_TIME_CONFLICT,-1)

            sql = 'insert into application(course_id,section_id,student_id,application_reason) '\
                'values(%s,%s,%s,%s)'
            print(sql)
            cursor.execute(sql,(course_id,section_id,user_id,app_reason,))
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)
  
    def execute(self):
       pass




