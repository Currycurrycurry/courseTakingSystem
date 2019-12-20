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
            user_id = self.data['user_id']
            course_id = self.data['course_id']
            section_id = self.data['section_id']
            status = self.data['status']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)
        
        try:
            cursor = connection.cursor()
            sql ="update application set status = " + status + " where course_id = '" +  course_id + "' and section_id = " + section_id
            print(sql)
            cursor.execute(sql)
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
            if row != None:
                self._init_response()
                return self._get_response(APP_ALREADY,-1)
            
            if row != None and row['if_drop'] == 1:
                self._init_response()
                return self._get_response(APP_DROPPED,-1)

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




