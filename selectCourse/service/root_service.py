import json
import traceback
from django.http import JsonResponse

from selectCourse.logs import logger
from selectCourse.util import sql_util
from django.db import connection
from selectCourse.constants.errorConstants import *
from selectCourse.constants.infoConstants import *
from selectCourse.service.base_service import BaseService

# ALL INSERT tested 12.13 by hjn
# ALL DELETE tested 12.13 by hjn
# ALL query tested 12.13 by hjn
# ALL UPDATE tested 12.13 by hjn


class RootService(BaseService):
    def __init__(self, request):
        super(RootService, self).__init__(request)
        if request.method == 'POST':
            self.data = request.POST

#################Course##################
    def deleteCourse(self):
        if self.request.session['is_login'] != True or \
            (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)
        
        try:
            course_id = self.data['course_id']

    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from course where course_id = %s'
            cursor.execute(sql,(course_id,))
            courses = sql_util.dictfetchone(cursor)

            if courses == None:
                self._init_response()
                return self._get_response("delete nonexist course",-1)

            sql = 'delete from course where course_id = %s'
            cursor.execute(sql,(course_id,))
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)
            
    def insertCourse(self):
        if self.request.session['is_login'] != True or \
            (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED) 

        try:
            course_id = self.data['course_id']
            title = self.data['title']
            credits = self.data['credits']
            dept_name = self.data['dept_name']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from course where course_id = %s'
            cursor.execute(sql,(course_id,))
            test = sql_util.dictfetchone(cursor)
            if test != None:
                self._init_response()
                return self._get_response("insert error: already exist",-1)
            sql = 'insert into course(course_id,title,credits,dept_name) values(%s,%s,%s,%s)'
            cursor.execute(sql,(course_id,title,credits,dept_name,))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)
        
    def checkCourses(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:

            page_num = int(self.data['current_page_num']) #0,1,2,...
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            check_all_courses_sql = "SELECT * FROM 'course' limit %s,%s"
            # start_page = ITEM_NUM_FOR_ONE_PAGE * page_num
            # print("start page is ",start_page)
            cursor.execute(check_all_courses_sql,(ITEM_NUM_FOR_ONE_PAGE * page_num,ITEM_NUM_FOR_ONE_PAGE,))
            raw_courses = sql_util.dictfetchall(cursor)
            print("raw courses are :",raw_courses)
            total_num_sql = 'select count(*) from course'
            cursor.execute(total_num_sql)
            total_num = int(cursor.fetchone()[0])
            print("total num is ",total_num)
            # sections = list(raw_courses_taken)
            sections = []
            for row in raw_courses:
                tmp = {
                    'title':row['title'],
                    'course_id':row['course_id'],
                    'credits':row['credits'],
                    'dept_name':row['dept_name'],
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





        pass
   
    def updateCourse(self):
        if self.request.session['is_login'] != True or \
            (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED) 

        try:
            course_id = self.data['course_id']
            title = self.data['title']
            credits = self.data['credits']
            dept_name = self.data['dept_name']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from course where course_id = %s'
            cursor.execute(sql,(course_id,))
            test = sql_util.dictfetchone(cursor)
            if test == None:
                self._init_response()
                return self._get_response(UPDATE_ERROR,-1)
            sql = 'update course set title=%s,credits=%s,dept_name=%s where course_id = %s'
            cursor.execute(sql,(title,credits,dept_name,course_id,))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

        pass 

################Section###################
    def deleteSection(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)
        
        try:
            course_id = self.data['course_id']
            section_id = self.data['section_id']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from section where course_id = %s and section_id = %s'
            cursor.execute(sql,(course_id,section_id,))
            courses = sql_util.dictfetchone(cursor)

            if courses == None:
                self._init_response()
                return self._get_response("delete nonexist section",-1)
            sql = 'delete from section where course_id = %s and section_id = %s'
            cursor.execute(sql,(course_id,section_id))
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)
        
    def insertSection(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            course_id = self.data['course_id']
            section_id = self.data['section_id']
            time = self.data['time']
            classroom_no = self.data['classroom_no']
            lesson = self.data['lesson']
            limit = self.data['limit']
            day = self.data['day']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from section where course_id = %s and section_id = %s'
            cursor.execute(sql,(course_id,section_id,))
            test = sql_util.dictfetchone(cursor)
            if test != None:
                self._init_response()
                return self._get_response("insert error: already exist",-1)

            sql = 'select * from course where course_id = %s'
            cursor.execute(sql,(course_id,))
            test = sql_util.dictfetchone(cursor)
            if test == None:
                self._init_response()
                return self._get_response("insert error: no such course",-1)

            sql = 'select * from classroom where classroom_no = %s'
            cursor.execute(sql,(classroom_no,))
            test = sql_util.dictfetchone(cursor)
            if test == None:
                self._init_response()
                return self._get_response("insert error: no such classroom",-1)

            sql = 'insert into section(course_id,section_id,time,classroom_no,lesson,`limit`,day) values(%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql,(course_id,section_id,time,classroom_no,lesson,limit,day,))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

    def checkSections(self):


        if self.request.session['is_login'] != True or \
            (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:

            page_num = int(self.data['current_page_num']) #0,1,2,...
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            check_all_courses_sql = "SELECT * FROM 'section' limit %s,%s"
            cursor.execute(check_all_courses_sql,(page_num*ITEM_NUM_FOR_ONE_PAGE,ITEM_NUM_FOR_ONE_PAGE,))
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
                    'course_id':row['course_id'],
                    'section_id':row['section_id'],
                    'limit':row['limit'],
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
   
    def updateSection(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            course_id = self.data['course_id']
            section_id = self.data['section_id']
            time = self.data['time']
            classroom_no = self.data['classroom_no']
            lesson = self.data['lesson']
            limit = self.data['limit']
            day = self.data['day']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from section where course_id = %s and section_id = %s'
            cursor.execute(sql,(course_id,section_id,))
            test = sql_util.dictfetchone(cursor)
            if test == None:
                self._init_response()
                return self._get_response(UPDATE_ERROR,-1)

            sql = 'select * from classroom where classroom_no = %s'
            cursor.execute(sql,(classroom_no,))
            test = sql_util.dictfetchone(cursor)
            if test == None:
                self._init_response()
                return self._get_response("insert error: no such classroom",-1)

            sql = 'update section set time=%s,classroom_no=%s,lesson=%s,`limit`=%s,day=%s where course_id=%s and section_id=%s'
            cursor.execute(sql,(time,classroom_no,lesson,limit,day,course_id,section_id,))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

        pass 

############Student######################

    def deleteStudent(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)
        
        try:
            student_id = self.data['student_id']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from student where student_id = %s'
            cursor.execute(sql,(student_id,))
            students = sql_util.dictfetchone(cursor)

            if students == None:
                self._init_response()
                return self._get_response("delete nonexist student",-1)

            sql = 'delete from student where student_id = %s'
            cursor.execute(sql,(student_id,))
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)
        
    def insertStudent(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            student_id = self.data['student_id']
            student_name = self.data['student_name']
            student_major = self.data['student_major']
            student_dept_name = self.data['student_dept_name']
            student_total_credit = self.data['student_total_credit']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from student where student_id = %s'
            cursor.execute(sql,(student_id,))
            test = sql_util.dictfetchone(cursor)
            if test != None:
                self._init_response()
                return self._get_response("insert error: already exist",-1)

            sql = 'select * from account where id = %s'
            cursor.execute(sql,(student_id,))
            test = sql_util.dictfetchone(cursor)
            if test == None:
                self._init_response()
                return self._get_response("insert error: no such account",-1)

            sql = 'insert into student(student_id,student_name,student_major,student_dept_name,student_total_credit)'\
                            'values(%s,%s,%s,%s,%s)'
            cursor.execute(sql,(student_id,student_name,student_major,student_dept_name,student_total_credit))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

    def checkStudents(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:

            page_num = int(self.data['current_page_num']) #0,1,2,...
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            check_all_courses_sql = "SELECT * FROM student limit %s,%s"
            start_page = page_num * ITEM_NUM_FOR_ONE_PAGE
            cursor.execute(check_all_courses_sql,(start_page,ITEM_NUM_FOR_ONE_PAGE,))
            raw_courses = sql_util.dictfetchall(cursor)
            print("raw students are :",raw_courses)
            total_num_sql = 'select count(*) from student'
            cursor.execute(total_num_sql)
            total_num = int(cursor.fetchone()[0])
            print("total num is ",total_num)
            # sections = list(raw_courses_taken)
            sections = []
            for row in raw_courses:
                tmp = {
                    'student_id':row['student_id'],
                    'student_name':row['student_name'],
                    'student_major':row["student_major"],
                    'student_dept_name':row["student_dept_name"],
                    'student_total_credit':row["student_total_credit"],
                }
                sections.append(tmp)

            res = {
                'total_num':total_num,
                'sections':sections,
            }
           
            self.response.update(res)
            self._init_response()
            return self._get_response(SHOW_PERSONAL_INFO,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

    def updateStudent(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            student_id = self.data['student_id']
            student_name = self.data['student_name']
            student_major = self.data['student_major']
            student_dept_name = self.data['student_dept_name']
            student_total_credit = self.data['student_total_credit']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from student where student_id = %s'
            cursor.execute(sql,(student_id,))
            test = sql_util.dictfetchone(cursor)
            if test == None:
                self._init_response()
                return self._get_response(UPDATE_ERROR,-1)

            sql = 'update student set student_name=%s,student_major=%s,student_dept_name=%s,student_total_credit=%s where student_id=%s'
            cursor.execute(sql,(student_name,student_major,student_dept_name,student_total_credit,student_id,))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

############Instructor######################

    def updateInstructor(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            instructor_id = self.data['instructor_id']
            instructor_name = self.data['instructor_name']
            instructor_class = self.data['instructor_class']
            dept_name = self.data['dept_name']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from instructor where instructor_id = %s'
            cursor.execute(sql,(instructor_id,))
            test = sql_util.dictfetchone(cursor)

            if test == None:
                self._init_response()
                return self._get_response(UPDATE_ERROR,-1)


      

            sql = 'update instructor set instructor_name=%s,instructor_class=%s,dept_name=%s where instructor_id=%s'
            cursor.execute(sql,(instructor_name,instructor_class,dept_name,instructor_id,))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

    def deleteInstructor(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)
        
        try:
            instructor_id = self.data['instructor_id']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from instructor where instructor_id = %s'
            cursor.execute(sql,(instructor_id,))
            instructors = sql_util.dictfetchone(cursor)

            if instructors == None:
                self._init_response()
                return self._get_response("delete nonexist instructor",-1)

            sql = 'delete from instructor where instructor_id = %s'
            cursor.execute(sql,(instructor_id,))
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)
        

    def insertInstructor(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            instructor_id = self.data['instructor_id']
            instructor_name = self.data['instructor_name']
            instructor_class = self.data['instructor_class']
            dept_name = self.data['dept_name']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from instructor where instructor_id = %s'
            cursor.execute(sql,(instructor_id,))
            test = sql_util.dictfetchone(cursor)

            if test != None:
                self._init_response()
                return self._get_response("insert error: already exist",-1)


            sql = 'select * from account where id = %s'
            cursor.execute(sql,(instructor_id,))
            test = sql_util.dictfetchone(cursor)

            if test == None:
                self._init_response()
                return self._get_response("insert error: no such account",-1)

            sql = 'insert into instructor(instructor_id,instructor_name,instructor_class,dept_name)'\
                            'values(%s,%s,%s,%s)'
            cursor.execute(sql,(instructor_id,instructor_name,instructor_class,dept_name))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)


    def checkInstructors(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:

            page_num = int(self.data['current_page_num']) #0,1,2,...
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            check_all_courses_sql = "SELECT * FROM instructor limit %s,%s"
            cursor.execute(check_all_courses_sql,(page_num*ITEM_NUM_FOR_ONE_PAGE,ITEM_NUM_FOR_ONE_PAGE,))
            raw_courses = sql_util.dictfetchall(cursor)
            print("raw instructor are :",raw_courses)
            total_num_sql = 'select count(*) from instructor'
            cursor.execute(total_num_sql)
            total_num = int(cursor.fetchone()[0])
            print("total num is ",total_num)
            sections = list(raw_courses)

            res = {
                'total_num':total_num,
                'sections':sections,
            }
           
            self.response.update(res)
            self._init_response()
            return self._get_response(SHOW_PERSONAL_INFO,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)


############Exam######################


    
    def checkExams(self):

        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:

            page_num = int(self.data['current_page_num']) #0,1,2,...
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            check_all_courses_sql = "SELECT * FROM exam limit %s,%s"
            cursor.execute(check_all_courses_sql,(page_num*ITEM_NUM_FOR_ONE_PAGE,ITEM_NUM_FOR_ONE_PAGE,))
            raw_courses = sql_util.dictfetchall(cursor)
            print("raw exam are :",raw_courses)
            total_num_sql = 'select count(*) from exam'
            cursor.execute(total_num_sql)
            total_num = int(cursor.fetchone()[0])
            print("total num is ",total_num)
            sections = list(raw_courses)

            res = {
                'total_num':total_num,
                'sections':sections,
            }
           
            self.response.update(res)
            self._init_response()
            return self._get_response(SHOW_PERSONAL_INFO,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)
    def insertExam(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            course_id = self.data['course_id']
            section_id = self.data['section_id']
            classroom_no = self.data['classroom_no']
            day = self.data['day']
            type = self.data["type"]
            start_time = self.data['start_time']
            end_time = self.data['end_time']
            open_note_flag = self.data['open_note_flag']
         
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from section where course_id = %s and section_id = %s'
            cursor.execute(sql,(course_id,section_id,))
            test = sql_util.dictfetchone(cursor)
            if test == None:
                self._init_response()
                return self._get_response(INSERT_ERROR,-1)

            sql = 'select * from classroom where classroom_no = %s'
            cursor.execute(sql,(classroom_no,))
            test = sql_util.dictfetchone(cursor)
            if test == None:
                self._init_response()
                return self._get_response(INSERT_ERROR,-1)

            sql = 'insert into  exam(course_id,section_id,classroom_no,day,type,start_time,end_time,open_note_flag'\
                'values(%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql,(course_id,section_id,classroom_no,day,type,start_time,end_time,open_note_flag,))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

    def deleteExam(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            course_id = self.data['course_id']
            section_id = self.data['section_id']
           
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from section where course_id = %s and section_id = %s'
            cursor.execute(sql,(course_id,section_id,))
            test = sql_util.dictfetchone(cursor)
            if test == None:
                self._init_response()
                return self._get_response("delete error: no such section",-1)

            sql = 'delete from exam where course_id=%s and section_id=%s'
            cursor.execute(sql,(course_id,section_id))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

    def updateExam(self):

        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            course_id = self.data['course_id']
            section_id = self.data['section_id']
            classroom_no = self.data['classroom_no']
            day = self.data['day']
            type = self.data["type"]
            start_time = self.data['start_time']
            end_time = self.data['end_time']
            open_note_flag = self.data['open_note_flag']
         
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from section where course_id = %s and section_id = %s'
            cursor.execute(sql,(course_id,section_id,))
            test = sql_util.dictfetchone(cursor)
            if test == None:
                self._init_response()
                return self._get_response(UPDATE_ERROR,-1)

            sql = 'select * from classroom where classroom_no = %s'
            cursor.execute(sql,(classroom_no,))
            test = sql_util.dictfetchone(cursor)
            if test == None:
                self._init_response()
                return self._get_response(UPDATE_ERROR,-1)

            sql = 'update exam set classroom_no=%s,day=%s,type=%s,start_time=%s,end_time=%s,open_note_flag=%s where course_id=%s and section_id=%s'
            cursor.execute(sql,(classroom_no,day,type,start_time,end_time,open_note_flag,course_id,section_id,))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)


        pass

###########Classroom##################
    def insertClassroom(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            classroom_no = self.data['classroom_no']
            capacity = self.data['capacity']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()


            sql = 'select * from classroom where classroom_no = %s'
            cursor.execute(sql,(classroom_no,))
            test = sql_util.dictfetchone(cursor)
            if test != None:
                self._init_response()
                return self._get_response("insert error: already exist",1)
            sql = 'insert into classroom(classroom_no,capacity)'\
                            'values(%s,%s)'
            cursor.execute(sql,(classroom_no,capacity))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

    def deleteClassroom(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)
        
        try:
            classroom_no= self.data['classroom_no']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from classroom where classroom_no = %s'
            cursor.execute(sql,(classroom_no,))
            instructors = sql_util.dictfetchone(cursor)

            if instructors == None:
                self._init_response()
                return self._get_response("delete nonexist classroom",-1)

            sql = 'delete from classroom where classroom_no = %s'
            cursor.execute(sql,(classroom_no,))
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)
        
    def checkClassrooms(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:

            page_num = int(self.data['current_page_num']) #0,1,2,...
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            check_all_courses_sql = "SELECT * FROM classroom limit %s,%s"
            cursor.execute(check_all_courses_sql,(page_num*ITEM_NUM_FOR_ONE_PAGE,ITEM_NUM_FOR_ONE_PAGE,))
            raw_courses = sql_util.dictfetchall(cursor)
            print("raw classroom  are :",raw_courses)
            total_num_sql = 'select count(*) from classroom'
            cursor.execute(total_num_sql)
            total_num = int(cursor.fetchone()[0])
            print("total num is ",total_num)
            sections = list(raw_courses)

            res = {
                'total_num':total_num,
                'sections':sections,
            }
           
           
            self.response.update(res)
            self._init_response()
            return self._get_response(SHOW_PERSONAL_INFO,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

        
        pass

    def updateClassroom(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            classroom_no = self.data['classroom_no']
            capacity = self.data['capacity']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()


            sql = 'select * from classroom where classroom_no = %s'
            cursor.execute(sql,(classroom_no,))
            test = sql_util.dictfetchone(cursor)
            if test == None:
                self._init_response()
                return self._get_response(UPDATE_ERROR,-1)
            sql = 'update classroom set capacity = %s where classroom_no=%s'             
            cursor.execute(sql,(capacity,classroom_no))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

        pass
  
###########Account#####################
    def insertAccount(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            user_id = self.data['user_id']
            password = self.data['password']
            role = self.data['role']

    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from account where id = %s'
            cursor.execute(sql,(user_id,))
            test = sql_util.dictfetchone(cursor)
            if test != None:
                self._init_response()
                return self._get_response("insert error: already exist",1)

            sql = 'insert into account(id,password,role)'\
                            'values(%s,%s,%s)'
            cursor.execute(sql,(user_id,password,role))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

    def deleteAccount(self):
        if self.request.session['is_login'] != True or \
            (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)
    
        try:
            user_id= self.data['user_id']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()


            sql = 'select * from account where id = %s'
            cursor.execute(sql,(user_id,))
            courses = sql_util.dictfetchone(cursor)

            if courses == None:
                self._init_response()
                return self._get_response("delete nonexist account",-1)

            sql = 'delete from account where id = %s'
            cursor.execute(sql,(user_id,))
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

    def checkAccounts(self):

        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:

            page_num = int(self.data['current_page_num']) #0,1,2,...
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            check_all_courses_sql = "SELECT * FROM account limit %s,%s"
            cursor.execute(check_all_courses_sql,(page_num*ITEM_NUM_FOR_ONE_PAGE,ITEM_NUM_FOR_ONE_PAGE,))
            raw_courses = sql_util.dictfetchall(cursor)
            print("raw account  are :",raw_courses)
            total_num_sql = 'select count(*) from account'
            cursor.execute(total_num_sql)
            total_num = int(cursor.fetchone()[0])
            print("total num is ",total_num)
            sections = list(raw_courses)

            res = {
                'total_num':total_num,
                'sections':sections,
            }
           
           
            self.response.update(res)
            self._init_response()
            return self._get_response(SHOW_PERSONAL_INFO,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

        
        pass
        
    def updateAccount(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            user_id = self.data['user_id']
            password = self.data['password']
            role = self.data['role']

    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from account where id = %s'
            cursor.execute(sql,(user_id,))
            test = sql_util.dictfetchone(cursor)
            if test != None:
                self._init_response()
                return self._get_response(UPDATE_ERROR,-1)

            sql = 'insert into account(id,password,role)'\
                            'values(%s,%s,%s)'
            cursor.execute(sql,(user_id,password,role))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

        pass