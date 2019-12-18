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

    # TODO can only be test after merging into the frontend
    def importExcel(self,request):
        if request.method == 'POST':
            # f = request.FILES['csvFile']
            f = request.FILES.get('excel_file')
            # type_excel = f.name.split('.')[1]
            # if type_excel in ['xlsx','xls']:
            wb = xlrd.open_workbook(filename=None,file_content=f.read())
            table = wb.sheets()[0]
            nrows = table.nrows
            rowValues = []
            try:
                for i in range(1,nrows): 
                    # ignore the excel head
                    rowValues.append(table.row_value(i))
            except Exception as e:
                self._init_response()
                self._get_response(ERROR_LOADING_FILE)
                print(str(e))
            # else:
            #     self._init_response()
            #     self._get_response(FILE_FORMAT_ERROR)
        else:
            self._init_response()
            self._get_response(POST_ARG_ERROR)
        return rowValues
    
    def registerScore(self):
        
        raw_student_scores = self.importExcel(self.request)
        if raw_student_scores != None:
            print("the student scores are ",raw_student_scores)
            try:
                cursor = connection.cursor()
                for row in raw_student_scores:
                    row = row.split(",")
                    if row[0]!=None and row[1]!=None and row[2]!=None and row[3]!=None:
                        course_id,section_id,student_id,grade = row[0],row[1],row[2],row[3]
                        sql = 'insert into takes(course_id,section_id,student_id,grade)'\
                            'values(%s,%s,%s,%s)'
                        cursor.execute(sql,( course_id,section_id,student_id,grade,))
            except Exception as error:
                traceback.print_exc()
                connection.rollback()
                self._init_response()
                return self._get_response(SERVER_ERROR,-1)

    def registerInstructor(self):

        raw_instructor_infos = importExcel(self.request)
        if raw_instructor_infos != None:
            print("the raw_instructor_infos are ",raw_instructor_infos)
            try:
                cursor = connection.cursor()
                for row in raw_instructor_infos:
                    row = row.split(",")
                    if row[0]!=None and row[1]!=None and row[2]!=None and row[3]!=None:
                        instructor_id,instructor_name,instructor_class,dept_name = row[0],row[1],row[2],row[3]
                        sql = 'insert into instructor(instructor_id,instructor_name,instructor_class,dept_name)'\
                            'values(%s,%s,%s,%s)'
                        cursor.execute(sql,(instructor_id,instructor_name,instructor_class,dept_name))
            except Exception as error:
                traceback.print_exc()
                connection.rollback()
                self._init_response()
                return self._get_response(SERVER_ERROR,-1)

    def registerStudent(self):
        raw_student_scores = self.importExcel(self.request)
        if raw_student_scores != None:
            print("the student scores are ",raw_student_scores)
            try:
                cursor = connection.cursor()
                for row in raw_student_scores:
                    row = row.split(",")
                    if row[0]!=None and row[1]!=None and row[2]!=None and row[3]!=None:
                        student_id,student_name,student_major,student_dept_name = row[0],row[1],row[2],row[3]
                        sql = 'insert into student(student_id,student_name,student_major,student_dept_name)'\
                            'values(%s,%s,%s,%s)'
                        cursor.execute(sql,(student_id,student_name,student_major,student_dept_name))
            except Exception as error:
                traceback.print_exc()
                connection.rollback()
                self._init_response()
                return self._get_response(SERVER_ERROR,-1)

    def registerCourse(self):

        raw_courses = importExcel(self.request)
        if raw_courses != None:
            print("the courses are ",raw_courses)
            try:
                cursor = connection.cursor()
                for row in raw_courses:
                    row = row.split(",")
                    if row[0]!=None and row[1]!=None and row[2]!=None and row[3]!=None:
                        course_id,title,credits,dept_name = row[0],row[1],row[2],row[3]
                        sql = 'insert into course(course_id,title,credits,dept_name)'\
                            'values(%s,%s,%s,%s)'
                        cursor.execute(sql,(course_id,title,credits,dept_name))
            except Exception as error:
                traceback.print_exc()
                connection.rollback()
                self._init_response()
                return self._get_response(SERVER_ERROR,-1)


    def registerSection(self):
        raw_sections = importExcel(self.request)
        if raw_sections != None:
            print("the sections are ",raw_sections)
            try:
                cursor = connection.cursor()
                for row in raw_sections:
                    row = row.split(",")
                    flag = True
                    for i in range(8):
                        if row[i]==None:
                            flag = False
                            break
                    if flag:
                        sql = 'insert into section(course_id,section_id,time,classroom_no,lesson,limit,day)'\
                            'values(%s,%s,%s,%s,%s,%s,%s)'
                        cursor.execute(sql,(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
            except Exception as error:
                traceback.print_exc()
                connection.rollback()
                self._init_response()
                return self._get_response(SERVER_ERROR,-1)


    def execute(self):
        pass



