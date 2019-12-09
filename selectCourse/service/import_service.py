import xlrd
import json
import traceback
from django.http import JsonResponse

from selectCourse.logs import logger
from selectCourse.util import sql_util
from django.db import connection
from selectCourse.constants.errorConstants import POST_ARG_ERROR,GET_ARG_ERROR,WRONG_PASSWD,WRONG_USERID,LOGIN_OK,LOGOUT_OK
from selectCourse.constants.infoConstants import *
from selectCourse.service.base_service import BaseService


class ImportService(BaseService):
    def __init__(self, request):
        super(ImportService, self).__init__(request)
        if request.method == 'POST':
            self.data = request.POST

    def importExcel(self,res,request):
        if request.method == 'POST':
            f = request.FILES['csvFile']
            type_excel = f.name.split('.')[1]
            if type_excel in ['xlsx','xls']:
                wb = xlrd.open_workbook(filename=None,file_content=f.read())
                table = wb.sheets()[0]
                nrows = table.nrows
                rowValues = []
                try:
                    for i in range(1,nrows):
                        # ignore the excel head
                        rowValues.append(table.row_value(i))
                except Exception as e:
                    res['msg'] = "error in loading"
                    res['code'] = 0
                    print(str(e))
            else:
                res['msg'] = "file type error: must be xlsx"
        else:
            res['msg'] = "must be post request"
        
        return rowValues
    def execute(self):
        try:
            user_id = self.data["user_id"]
            password = self.data["password"]
            # logger.info("user id is ",user_id)
            # logger.info("user password is ",password)
        except Exception as error:
            # logger.error(error)
            self._init_response(POST_ARG_ERROR)
            return self._get_response()

        try:
            cursor = connection.cursor()
            id_sql = 'select * from account where id = %s'
            cursor.execute(id_sql, (user_id,))
            row = sql_util.dictfetchone(cursor)
            if row is None:
                self._init_response()
                return self._get_response(WRONG_USERID,-1)
            else:
                pass_sql = 'select * from account where id = %s and password = %s '
                cursor.execute(pass_sql,(user_id,password))
                row = sql_util.dictfetchone(cursor)
                print(row)
                if row is None:
                    self._init_response()
                    return self._get_response(WRONG_PASSWD,-1)
                else:
                    role_num = row['role']
                    if role_num == STUDENT_ROLE:
                        find_student_name_sql = "SELECT 'student'.'student_name' FROM 'student' WHERE 'student'.'student_id' = '"+user_id+"'"
                        cursor.execute(find_student_name_sql)
                        raw_student_name = sql_util.dictfetchone(cursor)
                        res_name= raw_student_name["student_name"]
                        # logger.info(res_name)

                    if role_num == INSTRUCTOR_ROLE:
                        find_instructor_name_sql = "SELECT 'instructor'.'instructor_name' FROM 'instructor' WHERE 'instructor'.'instructor_id' = '"+user_id+"'"
                        cursor.execute(find_instructor_name_sql)
                        raw_instructor_name = sql_util.dictfetchone(cursor)
                        res_name= raw_instructor_name["instructor_name"]
                        # logger.info(res_name)

                    if role_num == ROOT_ROLE:
                        res_name = "administrator"

                    data = {'user_name':res_name,
                            'role':role_num}
                    self.request.session['user_id'] = user_id
                    self.request.session['role'] = row['role']
                    self.request.session['is_login'] = True
                    self.response.update(data)
                    self._init_response()
                    return self._get_response(LOGIN_OK,1)

        except Exception as error:
            traceback.print_exc()
            # logger.error(error)
            connection.rollback()
            self._init_response()
            return self._get_response(str(error))

    def logout(self):
        self.request.session.flush()
        self._init_response()
        return self._get_response(LOGOUT_OK,1)



