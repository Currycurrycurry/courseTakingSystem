import xlrd
import json
import traceback
from django.http import JsonResponse

from selectCourse.logs import logger
from selectCourse.util import sql_util
from django.db import connection
from selectCourse.constants.errorConstants import *
from selectCourse.constants.infoConstants import *
from selectCourse.service.base_service import BaseService


class ImportService(BaseService):
    def __init__(self, request):
        super(ImportService, self).__init__(request)
        if request.method == 'POST':
            self.data = request.POST


    def importExcel(self,request):
        if request.method == 'POST':  
            f = request.FILES.get('excel_file')
            wb = xlrd.open_workbook(filename=None,file_contents=f.read())
            table = wb.sheets()[0]
            nrows = table.nrows
            rowValues = []
            try:
                for i in range(1,nrows): 
                    # ignore the excel head
                    rowValues.append(table.row_values(i))
            except Exception as e:
                self._init_response()
                self._get_response(ERROR_LOADING_FILE)
                print(str(e))

        else:
            self._init_response()
            self._get_response(POST_ARG_ERROR)
        return rowValues
    
    # test ok
    def registerScore(self):  
        if self.request.session['is_login'] != True or (self.request.session['role'] != ROOT_ROLE and self.request.session['role']!=INSTRUCTOR_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)
        raw_student_scores = self.importExcel(self.request)
        if raw_student_scores != None:
            print("the student scores are ",raw_student_scores)
            try:
                cursor = connection.cursor()
           
                res = {"successed_item_num":0}
                for row in raw_student_scores:
                    if (row[0]!=None and row[1]!=None and row[2]!=None and row[3]!=None)\
                        and (row[0]!='' and row[1]!='' and row[2]!='' and row[3]!=''):
                        course_id,section_id,student_id,grade = row[0],int(row[1]),str(int(row[2])),row[3]

                        # 1. whether exist conflict
                        # (1) account
                        print("the student_id is ",student_id)
                        sql = 'select * from account where ID=%s'
                        cursor.execute(sql,(student_id,))
                        flag = sql_util.dictfetchone(cursor)
                        if flag == None:
                            msg = "no such account: "+str(student_id)
                            self._init_response()
                 
                            self.response.update(res)
                            return self._get_response(msg,-1)
                            
                        # (2) student
                        sql = 'select * from student where student_id=%s'
                        cursor.execute(sql,(student_id,))
                        flag = sql_util.dictfetchone(cursor)
                        if flag == None:
                            msg = "no such student: "+str(student_id)
                            self._init_response()
                      
                            self.response.update(res)
                            return self._get_response(msg,-1)
                        
                        # (3) course 
                        sql = 'select * from course where course_id=%s'
                        cursor.execute(sql,(course_id,))
                        flag = sql_util.dictfetchone(cursor)
                        if flag == None:
                            msg = "no such course: "+str(course_id)
                            self._init_response()
                      
                            self.response.update(res)
                            return self._get_response(msg,-1)

                        # (4) section
                        sql = 'select * from section where section_id=%s and course_id=%s'
                        cursor.execute(sql,(section_id,course_id,))
                        flag = sql_util.dictfetchone(cursor)
                        if flag == None:
                            msg = "no such section: "+str(course_id)+"."+str(section_id)
                            self._init_response()
                            self.response.update(res)
                            return self._get_response(msg,-1)

                        # (5) takes
                        sql = 'select * from takes where course_id=%s and section_id=%s and student_id=%s'
                        cursor.execute(sql,(course_id,section_id,student_id,))
                        flag = sql_util.dictfetchone(cursor)
                        if flag == None:
                            msg = "no such taking record: "+str(course_id)+"."+str(section_id)+" for "+str(student_id)
                            self._init_response()
                            self.response.update(res)
                            return self._get_response(msg,-1)
                 
                        # 2. insert the same data conflict
                        sql = 'select * from takes where course_id=%s and section_id=%s and student_id=%s and grade=%s'
                        cursor.execute(sql,(course_id,section_id,student_id,grade,))
                        if_has = sql_util.dictfetchone(cursor)
                        if if_has != None:
                            continue
                            
                        # 3. insert while should be update conflict —— 
                        sql = 'select * from takes where course_id=%s and section_id=%s and student_id=%s'
                        cursor.execute(sql,(course_id,section_id,student_id,))
                        if_has = sql_util.dictfetchone(cursor)
                        if if_has != None:
                            msg = "data conflict: " + course_id+"."+str(section_id)+" : "+ str(student_id)
                            self._init_response()
                      
                            self.response.update(res)
                            return self._get_response(msg,-1)
                        else:
                            sql = 'insert into takes(course_id,section_id,student_id,grade)'\
                                'values(%s,%s,%s,%s)'
                            cursor.execute(sql,( course_id,section_id,student_id,grade,))
                            res['successed_item_num']+=1
                    else:
                        self._init_response()
                        self.response.update(res)
                        return self._get_response(INVALID_BLANK,-1)
                self._init_response()
                self.response.update(res)
                return self._get_response(IMPORT_OK,1)

            except Exception as error:
                traceback.print_exc()
                connection.rollback()
                self._init_response()
                return self._get_response(SERVER_ERROR,-1)

    # test ok
    def registerInstructor(self):
        if self.request.session['is_login'] != True or self.request.session['role'] != ROOT_ROLE:
            self._init_response()
            return self._get_response(UNAUTHORIZED)
        raw_instructor_infos = self.importExcel(self.request)
      
        res = {"successed_item_num":0}
        if raw_instructor_infos != None:
            print("the raw_instructor_infos are ",raw_instructor_infos)
            try:
                cursor = connection.cursor()
                for row in raw_instructor_infos:
                    if (row[0]!=None and row[1]!=None and row[2]!=None and row[3]!=None)\
                        and (row[0]!='' and row[1]!='' and row[2]!='' and row[3]!=''):
                        instructor_id,instructor_name,instructor_class,dept_name = row[0],row[1],row[2],row[3]

                        # exist check
                        sql = 'select * from account where ID=%s'
                        cursor.execute(sql,(instructor_id,))
                        flag = sql_util.dictfetchone(cursor)
                        if flag == None:
                            sql = 'insert into account(ID,password,role) values(%s,%s,%s)'
                            cursor.execute(sql,(instructor_id,instructor_id,2))
                            
                        # same data check
                        sql = 'select * from instructor where instructor_id = %s'
                        cursor.execute(sql,(instructor_id,))
                        flag = sql_util.dictfetchone(cursor)
                        if flag == None:
                            sql = 'insert into instructor(instructor_id,instructor_name,instructor_class,dept_name)'\
                                'values(%s,%s,%s,%s)'
                            cursor.execute(sql,(instructor_id,instructor_name,instructor_class,dept_name))
                            res["successed_item_num"]+=1
                        else:
                            msg = "data conflict: " + instructor_id
                            
                            self._init_response()
                            self.response.update(res)
                            return self._get_response(msg,-1)
                        
                    else:
                        self._init_response()
                        self.response.update(res)
                        return self._get_response(INVALID_BLANK,-1)
                self._init_response()
               
                self.response.update(res)
                return self._get_response(IMPORT_OK,1)
            except Exception as error:
                traceback.print_exc()
                connection.rollback()
                self._init_response()
                return self._get_response(SERVER_ERROR,-1)
    # test ok
    def registerStudent(self):
        if self.request.session['is_login'] != True or self.request.session['role'] != ROOT_ROLE:
            self._init_response()
            return self._get_response(UNAUTHORIZED)
        raw_student_scores = self.importExcel(self.request)
        res = {"successed_item_num":0}
        if raw_student_scores != None:
            print("the student scores are ",raw_student_scores)
            try:
                cursor = connection.cursor()
                for row in raw_student_scores:
                    if (row[0]!=None and row[1]!=None and row[2]!=None and row[3]!=None)\
                        and (row[0]!='' and row[1]!='' and row[2]!='' and row[3]!='') :
                        student_id,student_name,student_major,student_dept_name = str(int(row[0])),row[1],row[2],row[3]

                        # exist check
                        sql = 'select * from account where ID=%s'
                        cursor.execute(sql,(student_id,))
                        flag = sql_util.dictfetchone(cursor)
                        if flag == None:
                            sql = 'insert into account(ID,password,role) values(%s,%s,%s)'
                            cursor.execute(sql,(student_id,student_id,1))
                            
                        # same data check
                        sql = 'select * from student where student_id = %s'
                        cursor.execute(sql,(student_id,))
                        flag = sql_util.dictfetchone(cursor)

                        if flag == None:
                            sql = 'insert into student(student_id,student_name,student_major,student_dept_name,student_total_credit)'\
                                'values(%s,%s,%s,%s,%s)'
                            cursor.execute(sql,(student_id,student_name,student_major,student_dept_name,0))
                            res["successed_item_num"]+=1
                        else:
                            self._init_response()
                            msg = "data conflict: "+student_id
                            self.response.update(res)
                            return self._get_response(msg,-1)
                 
                self._init_response()
                return self._get_response(IMPORT_OK,1)
            except Exception as error:
                traceback.print_exc()
                connection.rollback()
                self._init_response()
                return self._get_response(SERVER_ERROR,-1)
    # test ok
    def registerCourse(self):
        if self.request.session['is_login'] != True or self.request.session['role'] != ROOT_ROLE:
            self._init_response()
            return self._get_response(UNAUTHORIZED)
        raw_courses = self.importExcel(self.request)
        res = {'successed_item_num':0}
        if raw_courses != None:
            print("the courses are ",raw_courses)
            try:
                cursor = connection.cursor()
                for row in raw_courses:
                    if (row[0]!=None and row[1]!=None and row[2]!=None and row[3]!=None)\
                        and(row[0]!='' and row[1]!='' and row[2]!='' and row[3]!=''):
                        course_id,title,credits,dept_name = row[0],row[1],str(int(row[2])),row[3]
                        # same check
                        sql = 'select * from course where course_id=%s'
                        cursor.execute(sql,(course_id,))
                        flag = sql_util.dictfetchone(cursor)
                        if flag == None:
                            sql = 'insert into course(course_id,title,credits,dept_name)'\
                            'values(%s,%s,%s,%s)'
                            cursor.execute(sql,(course_id,title,credits,dept_name))
                            res['successed_item_num']+=1
                        else:
                            self._init_response()
                            msg = 'data conflict: '+course_id
                            self.response.update(res)
                            return self._get_response(msg,1)
                            
                self._init_response()
                return self._get_response(IMPORT_OK,1)
     
            except Exception as error:
                traceback.print_exc()
                connection.rollback()
                self._init_response()
                return self._get_response(SERVER_ERROR,-1)
    # test ok
    def registerSection(self):
        if self.request.session['is_login'] != True or self.request.session['role'] != ROOT_ROLE:
            self._init_response()
            return self._get_response(UNAUTHORIZED)
        raw_sections = self.importExcel(self.request)
        res = {'successed_item_num':0}
        if raw_sections != None:
            print("the sections are ",raw_sections)
            try:
                cursor = connection.cursor()
                for row in raw_sections:
                    flag = True
                    for i in range(8):
                        if row[i]==None:
                            flag = False
                            self._init_response()
                            return self._get_response(INVALID_BLANK,-1)
                            break
                    if flag:

                        # exist check
                        sql = 'select * from course where course_id =%s'
                        cursor.execute(sql,(row[0],))
                        flag = sql_util.dictfetchone(cursor)
                        if flag == None:
                            msg = "no such course: "+str(row[0])
                            self._init_response()
                            return self._get_response(msg,-1)
                        
                        # same check
                        sql = 'select * from section where course_id=%s and section_id=%s'
                        cursor.execute(sql,(row[0],row[1]))
                        flag = sql_util.dictfetchone(cursor)
                        if flag == None:
                            sql = 'insert into section(course_id,section_id,start,end,classroom_no,`limit`,day)'\
                                'values(%s,%s,%s,%s,%s,%s,%s)'
                            cursor.execute(sql,(row[0],str(int(row[1])),str(int(row[2])),str(int(row[3])),row[4],str(int(row[6])),str(int(row[7]))))
                            res['successed_item_num']+=1
                        else:
                            self._init_response()
                            self.response.update(res)
                            msg = "data conflict: "+ row[0]+"."+str(int(row[1]))
                            return self._get_response(msg,1)
                            
                self._init_response()
                return self._get_response(IMPORT_OK,1)
        
            except Exception as error:
                traceback.print_exc()
                connection.rollback()
                self._init_response()
                return self._get_response(SERVER_ERROR,-1)
        else:
            self._init_response()
            return self._get_response(INVALID_BLANK,-1)

    def execute(self):
        pass



