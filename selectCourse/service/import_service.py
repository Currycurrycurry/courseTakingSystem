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
        print(self.request.session['role'])
        if self.request.session['is_login'] != True or self.request.session['role'] != INSTRUCTOR_ROLE:
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
                        if flag == None: # 没有选课这直接报错
                            msg = "no such taking record: "+str(course_id)+"."+str(section_id)+" for "+str(student_id)
                            self._init_response()
                            self.response.update(res)
                            return self._get_response(msg,-1)
                        else: # 选过课程则更新成绩
                            sql = 'update takes set grade=%s where course_id=%s and section_id=%s and student_id=%s'
                            cursor.execute(sql,(grade, course_id,section_id,student_id,))
                            res['successed_item_num']+=1
                    else:
                        self._init_response()
                        self.response.update(res)
                        return self._get_response(INVALID_BLANK,-1)

                connection.commit()
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
                            
                        # same data check
                        sql = 'select * from instructor where instructor_id = %s'
                        cursor.execute(sql,(instructor_id,))
                        flag = sql_util.dictfetchone(cursor)
                        if flag == None:
                            sql = 'insert into instructor(instructor_id,instructor_name,instructor_class,dept_name)'\
                                'values(%s,%s,%s,%s)'
                            cursor.execute(sql,(instructor_id,instructor_name,instructor_class,dept_name))

                            sql = 'insert into account(id, password, role)'\
                                'values(%s,%s,%s)'
                            connection.commit()
                            cursor.execute(sql,(instructor_id, instructor_id, 2))
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

                            
                        # same data check
                        sql = 'select * from student where student_id = %s'
                        cursor.execute(sql,(student_id,))
                        flag = sql_util.dictfetchone(cursor)

                        if flag == None:
                            sql = 'insert into student(student_id,student_name,student_major,student_dept_name,student_total_credit)'\
                                'values(%s,%s,%s,%s,%s)'
                            cursor.execute(sql,(student_id,student_name,student_major,student_dept_name,0))

                            sql = 'insert into account(id, password, role)'\
                                'values(%s,%s,%s)'
                            cursor.execute(sql,(student_id,student_id, 1))
                            connection.commit()
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

                        print(course_id,title,credits,dept_name)
                        # same check
                        sql = 'select * from course where course_id="%s"'

                        cursor.execute(sql%(course_id,))
                        flag = sql_util.dictfetchone(cursor)

                        if flag == None:
                            sql = 'insert into course(course_id,title,credits,dept_name)'\
                            'values(%s,%s,%s,%s)'
                            cursor.execute(sql,(course_id,title,credits,dept_name))
                            connection.commit()
                            res['successed_item_num']+=1
                        else:
                            self._init_response()
                            msg = 'data conflict: '+course_id
                            self.response.update(res)
                            return self._get_response(msg, -1)
                            
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
                            self.response.update(res)
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
                            self.response.update(res)
                            return self._get_response(msg,-1)

                        sql = 'select * from classroom where classroom_no = %s'
                        cursor.execute(sql, (row[2],))
                        test = sql_util.dictfetchone(cursor)

                        if test == None:
                            self._init_response()
                            self.response.update(res)
                            return self._get_response("no such classroom:" + row[2], -1)

                        # TODO 老师的时空冲突检查 instructor_id 为 row[7]
                        sql = 'select * from teaches natural join section where instructor_id=%s'
                        cursor.execute(sql,(row[7],))
                        items = sql_util.dictfetchall(cursor)
                        if items != []:
                            for item in items:
                                day = int(item['day'])
                                start = int(item['start'])
                                end = int(item['end'])

                                t_day = int(row[6])
                                t_start = int(row[3])
                                t_end = int(row[4])
                                
                                if day == int(row[6]):
                                    if (start > t_start and start < t_end) or\
                                        (end > t_start and end < t_end):
                                        self._init_response()
                                        self.response.update(res)
                                        return self._get_response("instructor teaching time conflict: "+str(t_day)+":"+str(t_start)+"-"+str(t_end),-1)

                        # TODO 教室的时空冲突检查 classroom_no 为 row[2]
                        sql = 'select * from section where classroom_no=%s and day=%s and start=%s and end=%s'
                        cursor.execute(sql,(row[2],int(row[6],int(row[3]),int(row[4]))))
                        item = sql_util.dictfetchone(cursor)
                        if item != None:
                            self._init_response()
                            self.response.update(res)
                            return self._get_response("classroom time conflict: "+row[2],-1)
                        

                        sql = 'select * from teaches where course_id = %s and section_id=%s and instructor_id=%s'
                        cursor.execute(sql, (row[0],int(row[1]),row[7]))
                        test = sql_util.dictfetchone(cursor)

                        if test != None:
                            self._init_response()
                            self.response.update(res)
                            return self._get_response("data conflict:" +  row[0]+"."+ row[1], -1)

                        # same check
                        sql = 'select * from section where course_id=%s and section_id=%s'
                        cursor.execute(sql,(row[0],row[1]))
                        flag = sql_util.dictfetchone(cursor)

                        if flag == None:
                            sql = 'insert into section(course_id, section_id, classroom_no, start, `end`, `limit`, `day`)'\
                                'values(%s,%s,%s,%s,%s,%s,%s)'
                            cursor.execute(sql,(row[0], int(row[1]), row[2], int(row[3]), row[4], int(row[5]), int(row[6])))

                            # 同时插入teaches表
                            sql = 'insert into teaches(course_id, section_id, instructor_id)'\
                                'values(%s,%s,%s)'
                            cursor.execute(sql, (row[0], int(row[1]), row[7]))

                            connection.commit()
                            res['successed_item_num']+=1
                        else:
                            self._init_response()
                            self.response.update(res)
                            msg = "data conflict: "+ row[0]+"."+ row[1]
                            return self._get_response(msg, -1)
                            
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

    def registerExam(self):
        # if self.request.session['is_login'] != True or self.request.session['role'] != ROOT_ROLE:
        #     self._init_response()
        #     return self._get_response(UNAUTHORIZED)
        raw_exams = self.importExcel(self.request)
        res = {'successed_item_num':0}


        if raw_exams != None:
            print("the exams are ",raw_exams)
            try:
                cursor = connection.cursor()
                for row in raw_exams:
                    flag = True
                    for i in range(7):
                        if row[i]==None or row[i]=='':
                            flag = False
                            self._init_response()
                            return self._get_response(INVALID_BLANK,-1)
                            break
                    if flag:
                        t_course_id = row[0]
                        t_section_id = int(row[1])
                        t_type = int(row[2])
                        t_exam_day = int(row[3])
                        # t_start_time = int((str(row[4])).split(":")[0])
                        # t_end_time = int((str(row[5])).split(":")[0])
                        t_start_time = float(row[4])
                        t_end_time = float(row[5])
                        t_exam_classroon_no = str(row[6])
                        # exist check
                        sql = 'select * from course where course_id =%s'
                        cursor.execute(sql,(row[0],))
                        flag = sql_util.dictfetchone(cursor)
                        if flag == None:
                            msg = "no such course: "+str(row[0])
                            self._init_response()
                            return self._get_response(msg,-1)

                        sql = 'select * from classroom where classroom_no = %s'
                        cursor.execute(sql, (row[6],))
                        test = sql_util.dictfetchone(cursor)
                        if test == None:
                            self._init_response()
                            return self._get_response("no such classroom:" + row[2], -1)

                        sql = 'select * from section where course_id = %s and section_id=%s '
                        cursor.execute(sql, (row[0],int(row[1]),))
                        test = sql_util.dictfetchone(cursor)

                        if test == None:
                            self._init_response()
                            return self._get_response("no such section:" +  row[0]+"."+ row[1], -1)

                        sql = 'select * from exam where exam_day=%s and exam_classroom_no=%s'
                        cursor.execute(sql,(t_exam_day,t_exam_classroon_no,))
                        test = sql_util.dictfetchall(cursor)
                        if test != []:
                            for item in test:
                                test_start = float(int(item['start_time'].split(":")[0])/24)
                                test_end = float(int(item['end_time'].split(":")[0])/24)
                                if (test_start > t_start_time and test_start < t_end_time) or\
                                    (test_end > t_start_time and test_end < t_end_time):
                                    self._init_response()
                                    self.response.update(res)
                                    return self._get_response("exam classroom time conflict",-1)

                        # same check
                        sql = 'select * from exam where course_id=%s and section_id=%s'
                        cursor.execute(sql,(row[0],int(row[1])))
                        flag = sql_util.dictfetchone(cursor)

                        if flag == None:
                            sql = 'insert into exam(course_id, section_id, exam_classroom_no, exam_day, type, start_time, end_time, open_note_flag)'\
                                'values(%s,%s,%s,%s,%s,%s,%s,%s)'
                            cursor.execute(sql,(row[0], int(row[1]), row[6], int(row[3]), t_type,str(t_start_time*24),str(t_end_time*24),0))
                            connection.commit()
                            res['successed_item_num']+=1  
                        else:
                            self._init_response()
                            self.response.update(res)
                            msg = "data conflict: "+ row[0]+"."+ str(int(row[1]))
                            return self._get_response(msg, -1)
                            
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



