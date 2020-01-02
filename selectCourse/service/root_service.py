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
        elif request.method == 'GET':
            self.data = request.GET

#################Course##################
    def updateCourseStatus(self):
        if self.request.session['is_login'] != True or \
            (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            status = self.data['status']

        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR, -1)

        try:
            cursor = connection.cursor()

            sql = 'update course_status set status=%s'
            cursor.execute(sql,(status,))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)

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
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)
            
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
            return self._get_response(SERVER_ERROR,-1)
        
    def checkCourses(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            page_num = int(self.data['page_num']) #0,1,2,...
            course_id = self.data['course_id']
            title = self.data['title']
            dept_name = self.data['dept_name']
    
        except Exception as error:
            self._init_response()
            return self._get_response(GET_ARG_ERROR,-1)

        try:
            get_dict = self.data.copy() 
            del get_dict['page_num']
            print(get_dict)
            cursor = connection.cursor()

            sql = "SELECT * FROM 'course'"
            cnt_sql = 'select count(*) from course'
            sql_conditions = []
            for key in get_dict.keys():
                if get_dict[key]!=None and get_dict[key]!='':
                    sql_conditions.append(str(key+" like '%"+get_dict[key]+"%'"))
            if len(sql_conditions)==0:
                final_sql = sql
            else:
                final_sql = (sql+" where ")
                cnt_sql += " where "
                for i,condition in enumerate(sql_conditions):
                    if i != len(sql_conditions)-1:
                        final_sql += (condition + " and ")
                        cnt_sql += (condition + " and ")
                    else:
                        final_sql += condition
                        cnt_sql += condition

            final_sql += (" limit "+str(page_num*ITEM_NUM_FOR_ONE_PAGE)+","+str(ITEM_NUM_FOR_ONE_PAGE))

            print(final_sql)    
            cursor.execute(final_sql)
            rows = sql_util.dictfetchall(cursor)
            # print("rows are ",rows)

            cursor.execute(cnt_sql)
            total_num = int(cursor.fetchone()[0])
            print("total num is ",total_num)
            sections = []

            if len(rows)!=0:
            
                for row in rows:
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
            return self._get_response(SERVER_ERROR,-1)

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
            print(sql)
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)

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
            connection.commit()

            # 级联删除不需要考虑teaches,takes和其他冲突
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)
        
    def insertSection(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            course_id = self.data['course_id']
            section_id = self.data['section_id']
            start = self.data['start']
            end = self.data['end']
            instructor_id = self.data['instructor_id']
            classroom_no = self.data['classroom_no']
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
            cursor.execute(sql, (classroom_no,))
            test = sql_util.dictfetchone(cursor)
            if test == None:
                self._init_response()
                return self._get_response("insert error: no such classroom" + classroom_no, -1)

            sql = 'select * from instructor where instructor_id = %s'
            cursor.execute(sql, (instructor_id,))
            test = sql_util.dictfetchone(cursor)

            if test == None:
                self._init_response()
                return self._get_response("insert error: no such instructor " + instructor_id, -1)

             # TODO 老师的时空冲突检查 instructor_id 为 row[7]
            sql = 'select * from teaches natural join section where instructor_id=%s'
            cursor.execute(sql,(instructor_id,))
            items = sql_util.dictfetchall(cursor)
            if items != []:
                for item in items:
                    day = int(item['day'])
                    start = int(item['start'])
                    end = int(item['end'])

                    t_day = int(day)
                    t_start = int(start)
                    t_end = int(end)
                    
                    if t_day == day:
                        if (start > t_start and start < t_end) or\
                            (end > t_start and end < t_end):
                            self._init_response()
                            return self._get_response("instructor teaching time conflict: "+str(t_day)+":"+str(t_start)+"-"+str(t_end),-1)

            # TODO 教室的时空冲突检查 classroom_no 为 row[2]
            sql = 'select * from section where classroom_no=%s and day=%s and start=%s and end=%s'
            cursor.execute(sql,(classroom_no,int(day),int(start),int(end)))
            item = sql_util.dictfetchone(cursor)
            if item != None:
                self._init_response()
                return self._get_response("classroom time conflict: "+classroom_no,-1)

            sql = 'insert into section(course_id, section_id, start, `end`,classroom_no,`limit`,`day`) values(%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql,(course_id,section_id, start, end, classroom_no,limit,day,))

            #同时插入teaches表
            sql = 'insert into teaches(course_id, section_id, instructor_id) values(%s,%s,%s)'
            cursor.execute(sql,(course_id, section_id,instructor_id,))

            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)

    def checkSections(self):

        if self.request.session['is_login'] != True or \
            (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:

            page_num = int(self.data['page_num']) #0,1,2,...
            course_id = self.data['course_id']
            section_id = self.data['section_id']
            instructor_id = self.data['instructor_id']

        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            get_dict = self.data.copy() 
            del get_dict['page_num']
            print(get_dict)
            cursor = connection.cursor()

            sql = 'SELECT * FROM section natural join teaches where course_id like "%' + course_id + '%" and instructor_id like "%' + instructor_id + '%" '
            cnt_sql = 'SELECT count(*) FROM section natural join teaches where course_id like "%' + course_id + '%" and instructor_id like "%' + instructor_id + '%" '
            if int(section_id) != 0:
                sql += "and section_id=" + section_id
                cnt_sql += "and section_id=" + section_id
            sql += (" limit "+str(page_num*ITEM_NUM_FOR_ONE_PAGE)+","+str(ITEM_NUM_FOR_ONE_PAGE))

            cursor.execute(sql)
            rows = sql_util.dictfetchall(cursor)

            cursor.execute(cnt_sql)
            total_num = int(cursor.fetchone()[0])

            sections = []
            if len(rows)!=0:
                for row in rows:
                    tmp = {  
                        'course_id':row['course_id'],
                        'section_id':row['section_id'],
                        'limit':row['limit'],
                        'classroom_no':row['classroom_no'],
                        'day':row['day'],
                        'start':row['start'],
                        'end':row['end'],
                        'instructor_id': row['instructor_id'],
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
            return self._get_response(SERVER_ERROR,-1)
   
    def updateSection(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            course_id = self.data['course_id']
            section_id = self.data['section_id']
            start = self.data['start']
            end = self.data['end']
            instructor_id = self.data['instructor_id']
            classroom_no = self.data['classroom_no']
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
                return self._get_response("insert error: no such classroom" + classroom_no,-1)

            sql = 'select * from instructor where instructor_id = %s'
            cursor.execute(sql,(instructor_id,))
            test = sql_util.dictfetchone(cursor)

            if test == None:
                self._init_response()
                return self._get_response("insert error: no such instructor " + instructor_id,-1)

            # TODO 老师的时空冲突检查 instructor_id 为 row[7]
            sql = 'select * from teaches natural join section where instructor_id=%s'
            cursor.execute(sql,(instructor_id,))
            items = sql_util.dictfetchall(cursor)
            if items != []:
                for item in items:
                    day = int(item['day'])
                    start = int(item['start'])
                    end = int(item['end'])

                    t_day = int(day)
                    t_start = int(start)
                    t_end = int(end)
                    
                    if t_day == day:
                        if (start > t_start and start < t_end) or\
                            (end > t_start and end < t_end):
                            self._init_response()
                            return self._get_response("instructor teaching time conflict: "+str(t_day)+":"+str(t_start)+"-"+str(t_end),-1)

            # TODO 教室的时空冲突检查 classroom_no 为 row[2]
            sql = 'select * from section where classroom_no=%s and day=%s and start=%s and end=%s'
            cursor.execute(sql,(classroom_no,int(day),int(start),int(end)))
            item = sql_util.dictfetchone(cursor)
            if item != None:
                self._init_response()
                return self._get_response("classroom time conflict: "+classroom_no,-1)

            sql = 'update section set start=%s, end = %s, classroom_no=%s, `limit`=%s, `day`=%s where course_id=%s and section_id=%s'
            cursor.execute(sql,(start, end, classroom_no,  limit, day, course_id, section_id,))

            sql = 'update teaches set instructor_id=%s where course_id=%s and section_id=%s'
            cursor.execute(sql,(instructor_id,course_id, section_id,))

            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)

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

            # 同时删除学生和账户
            sql = 'delete from account where id = %s'
            cursor.execute(sql,(student_id,))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)
        
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


            sql = 'insert into student(student_id,student_name,student_major,student_dept_name)'\
                            'values(%s,%s,%s,%s)'
            cursor.execute(sql,(student_id,student_name,student_major,student_dept_name))

            sql = 'insert into account(id,password,role)'\
                            'values(%s,%s,%s)'
            cursor.execute(sql,(student_id, student_id, 1))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)

    def checkStudents(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            page_num = int(self.data['page_num']) #0,1,2,...
            student_id = self.data['student_id']
            student_name = self.data['student_name']
            student_major = self.data['student_major']

        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            get_dict = self.data.copy() 
            del get_dict['page_num']
            print(get_dict)
            cursor = connection.cursor()

            sql = "SELECT * FROM student"
            cnt_sql = 'select count(*) from student'
            sql_conditions = []
            for key in get_dict.keys():
                if get_dict[key]!=None and get_dict[key]!='':
                    sql_conditions.append(str(key+" like '%"+get_dict[key]+"%'"))
            if len(sql_conditions)==0:
                final_sql = sql
            else:
                final_sql = (sql+" where ")
                cnt_sql += " where "
                for i,condition in enumerate(sql_conditions):
                    if i != len(sql_conditions)-1:
                        final_sql += (condition + " and ")
                        cnt_sql += (condition + " and ")
                    else:
                        final_sql += condition
                        cnt_sql += condition

            final_sql += (" limit "+str(page_num*ITEM_NUM_FOR_ONE_PAGE)+","+str(ITEM_NUM_FOR_ONE_PAGE))

            print(final_sql)    
            cursor.execute(final_sql)
            rows = sql_util.dictfetchall(cursor)

            cursor.execute(cnt_sql)
            total_num = int(cursor.fetchone()[0])
            print("total num is ",total_num)
            students = []

            if len(rows)!=0:
                for row in rows:
                    tmp = {
                        'student_id':row['student_id'],
                        'student_name':row['student_name'],
                        'student_major':row["student_major"],
                        'student_dept_name':row["student_dept_name"],
                        'student_total_credit':row["student_total_credit"],
                    }
                    students.append(tmp)

            res = {
                'total_num':total_num,
                'students':students,
            }

            self.response.update(res)
            self._init_response()
            return self._get_response(SHOW_PERSONAL_INFO,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)

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
            return self._get_response(SERVER_ERROR,-1)

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
            return self._get_response(SERVER_ERROR,-1)

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

            sql = 'delete from account where id = %s'
            cursor.execute(sql,(instructor_id,))
            connection.commit()

            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)
        
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


            sql = 'insert into instructor(instructor_id,instructor_name,instructor_class,dept_name)'\
                            'values(%s,%s,%s,%s)'
            cursor.execute(sql,(instructor_id,instructor_name,instructor_class,dept_name))

            sql = 'insert into account(id, password, role)'\
                            'values(%s,%s,%s)'
            cursor.execute(sql,(instructor_id,instructor_id,2))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)

    def checkInstructors(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:

            page_num = int(self.data['page_num']) #0,1,2,...
            instructor_id = self.data['instructor_id']
            instructor_name = self.data['instructor_name']
            instructor_class = self.data['instructor_class']
            dept_name = self.data['dept_name']

    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            get_dict = self.data.copy() 
            del get_dict['page_num']
            print(get_dict)
            cursor = connection.cursor()
       
            sql = "SELECT * FROM instructor"
            cnt_sql = 'select count(*) from instructor'
            sql_conditions = []
            for key in get_dict.keys():
                if get_dict[key]!=None and get_dict[key]!='':
                    sql_conditions.append(str(key+" like '%"+get_dict[key]+"%'"))
            if len(sql_conditions)==0:
                final_sql = sql
            else:
                final_sql = (sql+" where ")
                cnt_sql += " where "
                for i,condition in enumerate(sql_conditions):
                    if i != len(sql_conditions)-1:
                        final_sql += (condition + " and ")
                        cnt_sql += (condition + " and ")
                    else:
                        final_sql += condition
                        cnt_sql += condition

            final_sql += (" limit "+str(page_num*ITEM_NUM_FOR_ONE_PAGE)+","+str(ITEM_NUM_FOR_ONE_PAGE))

            print(final_sql)    
            cursor.execute(final_sql)
            rows = sql_util.dictfetchall(cursor)
            # print("rows are ",rows)

            cursor.execute(cnt_sql)
            total_num = int(cursor.fetchone()[0])
            print("total num is ",total_num)

            instructors = []
            if len(rows)!=0:
                for row in rows:
                    tmp = {
                        'instructor_id':row['instructor_id'],
                        'instructor_name':row['instructor_name'],
                        'instructor_class':row['instructor_class'],
                        'dept_name':row['dept_name']
                    }
                    instructors.append(tmp)

            res = {
                'total_num':total_num,
                'instructors':instructors,
            }
           
            self.response.update(res)
            self._init_response()
            return self._get_response(SHOW_PERSONAL_INFO,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)


############Exam######################

    def checkExams(self):

        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:

            page_num = int(self.data['page_num']) #0,1,2,...
            course_id = self.data['course_id']
            section_id = self.data['section_id']
            exam_day = self.data['exam_day']
            type = self.data['type']
            
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            get_dict = self.data.copy() 
            del get_dict['page_num']
            cursor = connection.cursor()

            sql = 'SELECT * FROM exam where course_id like "%' + course_id + '%"  '
            cnt_sql = 'SELECT count(*) FROM exam where course_id like "%' + course_id + '%" '

            if int(section_id) != 0:
                sql += " and section_id=" + section_id
                cnt_sql += " and section_id=" + section_id

            if int(exam_day) != 0:
                sql += " and exam_day=" + exam_day
                cnt_sql += " and exam_day=" + exam_day

            if int(type) != -1:
                sql += " and type=" + type
                cnt_sql += " and type=" + type


            sql += (" limit "+str(page_num*ITEM_NUM_FOR_ONE_PAGE)+","+str(ITEM_NUM_FOR_ONE_PAGE))
            print(sql)
            cursor.execute(sql)
            rows = sql_util.dictfetchall(cursor)

            cursor.execute(cnt_sql)
            total_num = int(cursor.fetchone()[0])
            exams = []

            if len(rows)!=0:

                for row in rows:
                    tmp = {
                    "course_id" :row['course_id'],
                    "section_id":row['section_id'],
                    "exam_classroom_no":row['exam_classroom_no'],
                    "exam_day":row['exam_day'],
                    "type":row['type'],
                    "start_time":row['start_time'],
                    "end_time":row['end_time']
                    }
                    exams.append(tmp)

            res = {
                'total_num':total_num,
                'exams':exams,
            }
            self.response.update(res)
            self._init_response()
            return self._get_response(SHOW_PERSONAL_INFO,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)

    def insertExam(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            course_id = self.data['course_id']
            section_id = self.data['section_id']
            classroom_no = self.data['exam_classroom_no']
            day = self.data['exam_day']
            type = self.data["type"]
            start_time = self.data['start_time']
            end_time = self.data['end_time']
    
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

            sql = 'select * from exam where course_id = %s and section_id = %s'
            cursor.execute(sql,(course_id,section_id,))
            test = sql_util.dictfetchone(cursor)

            if test != None:
                self._init_response()
                return self._get_response(INSERT_ERROR,-1)

            if int(type) == 0:
                sql = 'select * from classroom where classroom_no = %s'
                cursor.execute(sql,(classroom_no,))
                test = sql_util.dictfetchone(cursor)
                if test == None:
                    self._init_response()
                    return self._get_response(INSERT_ERROR,-1)
                sql = 'insert into exam (course_id,section_id,exam_classroom_no,exam_day,`type`,start_time,end_time,open_note_flag)'\
                    'values(%s,%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(sql,(course_id, section_id, classroom_no, day, type, start_time, end_time, 0,))
            else:
                sql = 'insert into exam (course_id,section_id, exam_day,`type`,end_time)'\
                    'values(%s,%s,%s,%s,%s)'
                cursor.execute(sql,(course_id, section_id, day, type, end_time,))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)

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
            return self._get_response(SERVER_ERROR,-1)

    def updateExam(self):

        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED,-1)

        try:
            course_id = self.data['course_id']
            section_id = self.data['section_id']
            classroom_no = self.data['exam_classroom_no']
            day = self.data['exam_day']
            type = self.data["type"]
            start_time = self.data['start_time']
            end_time = self.data['end_time']
         
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from section where course_id = %s and section_id = %s'
            cursor.execute(sql,(course_id,section_id,))
            test = sql_util.dictfetchone(cursor)
            print(1)
            if test == None:
                self._init_response()
                return self._get_response(UPDATE_ERROR,-1)

            if int(type) == 1:
                sql = 'update exam set exam_day=%s,type=%s,start_time=%s,end_time=%s where course_id=%s and section_id=%s'
                cursor.execute(sql, (day, type, start_time, end_time, course_id, section_id,))
            else:
                sql = 'select * from classroom where classroom_no = %s'
                cursor.execute(sql,(classroom_no,))
                test = sql_util.dictfetchone(cursor)
                if test == None:
                    self._init_response()
                    return self._get_response(UPDATE_ERROR,-1)

                sql = 'update exam set exam_classroom_no=%s,exam_day=%s,type=%s,start_time=%s,end_time=%s where course_id=%s and section_id=%s'
                cursor.execute(sql,(classroom_no,day,type,start_time,end_time,course_id,section_id,))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)


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
            return self._get_response(SERVER_ERROR,-1)

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
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)

    def checkAccounts(self):

        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:

            page_num = int(self.data['page_num']) #0,1,2,...
            ID = self.data['id']
            password = self.data['password']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            get_dict = self.data.copy() 
            del get_dict['page_num']
            print(get_dict)
            cursor = connection.cursor()

            sql = 'select * from account'
            cnt_sql = 'select count(*) from account'
            sql_conditions = []
            for key in get_dict.keys():
                if get_dict[key]!=None and get_dict[key]!='':
                    sql_conditions.append(str(key+" like '%"+get_dict[key]+"%'"))
            if len(sql_conditions)==0:
                final_sql = sql
            else:
                final_sql = (sql+" where ")
                cnt_sql += " where "
                for i,condition in enumerate(sql_conditions):
                    if i != len(sql_conditions)-1:
                        final_sql += (condition + " and ")
                        cnt_sql += (condition + " and ")
                    else:
                        final_sql += condition
                        cnt_sql += condition

            final_sql += (" limit "+str(page_num*ITEM_NUM_FOR_ONE_PAGE)+","+str(ITEM_NUM_FOR_ONE_PAGE))

            print(final_sql)    
            cursor.execute(final_sql)
            rows = sql_util.dictfetchall(cursor)
            # print("rows are ",rows)

            cursor.execute(cnt_sql)
            total_num = int(cursor.fetchone()[0])
            print("total num is ",total_num)


            if len(rows)!=0:
                accounts = []
                for row in rows:
                    tmp = {
                        'id':row['ID'],
                        'password':row['password'],
                        'role':row['role']
                    }
                    accounts.append(tmp)

                res = {
                    'total_num':total_num,
                    'accounts':accounts,
                }
           
           
            self.response.update(res)
            self._init_response()
            return self._get_response(SHOW_PERSONAL_INFO,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)

        
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
            return self._get_response(SERVER_ERROR,-1)


###########Application#####################

    def checkApplications(self):
        if self.request.session['is_login'] != True or \
        (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)

        try:
            page_num = int(self.data['page_num']) #0,1,2,...
            course_id = self.data['course_id']
            section_id = self.data['section_id']
            student_id = self.data['student_id']
            application_reason = self.data['application_reason']


        except Exception as error:
            self._init_response()
            return self._get_response(GET_ARG_ERROR,-1)

        try:
            get_dict = self.data.copy() 
            del get_dict['page_num']
            print(get_dict)
            cursor = connection.cursor()

            sql = 'select * from application'
            cnt_sql = 'select count(*) from application'
            sql_conditions = []
            for key in get_dict.keys():
                if get_dict[key]!=None and get_dict[key]!='':
                    sql_conditions.append(str(key+" like '%"+get_dict[key]+"%'"))
            if len(sql_conditions)==0:
                final_sql = sql
            else:
                final_sql = (sql+" where ")
                cnt_sql += " where "
                for i,condition in enumerate(sql_conditions):
                    if i != len(sql_conditions)-1:
                        final_sql += (condition + " and ")
                        cnt_sql += (condition + " and ")
                    else:
                        final_sql += condition
                        cnt_sql += condition

            final_sql += (" limit "+str(page_num*ITEM_NUM_FOR_ONE_PAGE)+","+str(ITEM_NUM_FOR_ONE_PAGE))

            print(final_sql)    
            cursor.execute(final_sql)
            rows = sql_util.dictfetchall(cursor)
            # print("rows are ",rows)

            cursor.execute(cnt_sql)
            total_num = int(cursor.fetchone()[0])
            print("total num is ",total_num)

            if len(rows)!=0:
                applications = []
            
                for row in rows:
                    tmp = {
                     'course_id':row['course_id'],
                     'section_id':row['section_id'],
                     'student_id':row['student_id'],
                     'status':row['status'],
                     'application_reason':row['application_reaosn'],
                     'if_drop':row['if_drop']
                    }
                    applications.append(tmp)

                res = {
                    'total_num':total_num,
                    'applications':applications,
                }
            
                self.response.update(res)
                self._init_response()
                return self._get_response(SHOW_COURSES,1)
            else:
                self._init_response()
                return self._get_response(NO_RESULT,-1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)



        pass

    def deleteApplication(self):
        if self.request.session['is_login'] != True or \
            (self.request.session['role'] != ROOT_ROLE):
            self._init_response()
            return self._get_response(UNAUTHORIZED)
    
        try:
            user_id= self.data['user_id']
            course_id = self.data['course_id']
            section_id = self.data['section_id']
    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)

        try:
            cursor = connection.cursor()

            sql = 'select * from application where student_id = %s and course_id=%s and section_id=%s'
            cursor.execute(sql,(user_id,))
            courses = sql_util.dictfetchone(cursor)

            if courses == None:
                self._init_response()
                return self._get_response("delete nonexist application",-1)

            sql = 'delete from application where student_id = %s and course_id=%s and section_id=%s'
            cursor.execute(sql,(user_id,))
            connection.commit()
            self._init_response()
            return self._get_response(HANDLE_OK,1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR,-1)


    # def delete(self,tb_name,*pk):
    #     if self.request.session['is_login'] != True or \
    #         (self.request.session['role'] != ROOT_ROLE):
    #         self._init_response()
    #         return self._get_response(UNAUTHORIZED)
    
    #     try:
    #         user_id= self.data['user_id']
    
    #     except Exception as error:
    #         self._init_response()
    #         return self._get_response(POST_ARG_ERROR,-1)

    #     try:
    #         cursor = connection.cursor()


    #         sql = 'select * from '+tb_name+' where '+pk+' = %s'
    #         cursor.execute(sql,(pk,))
    #         courses = sql_util.dictfetchone(cursor)

    #         if courses == None:
    #             self._init_response()
    #             return self._get_response("delete nonexist account",-1)

    #         sql = 'delete from account where id = %s'
    #         cursor.execute(sql,(user_id,))
    #         self._init_response()
    #         return self._get_response(HANDLE_OK,1)

    #     except Exception as error:
    #         traceback.print_exc()
    #         connection.rollback()
    #         self._init_response()
    #         return self._get_response(SERVER_ERROR,-1)