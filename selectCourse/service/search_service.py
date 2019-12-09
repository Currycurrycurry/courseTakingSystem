import json
import traceback
from django.http import JsonResponse

from selectCourse.logs import logger
from selectCourse.util import sql_util
from django.db import connection
from selectCourse.constants.errorConstants import *
from selectCourse.constants.infoConstants import *
from selectCourse.service.base_service import BaseService

# TODO wait for more tests
class SearchService(BaseService):
    def __init__(self, request):
        super(SearchService, self).__init__(request)
        if request.method == 'POST':
            self.data = request.POST

    def execute(self):
        if self.request.session['is_login'] != True:
            self._init_response()
            return self._get_response(UNAUTHORIZED,-1)

        try:
            user_id = self.data['user_id']
            search_type = int(self.data['search_type'])


    
        except Exception as error:
            self._init_response()
            return self._get_response(POST_ARG_ERROR,-1)
        
        try:
            cursor = connection.cursor()
            if search_type == SEARCH_BY_SECTION:
                course_id = self.data['course_id']
                section_id = self.data['section_id']
                sql = 'select * from section natural join course natural join teaches natural join instructor where course_id = %s and section_id = %s'
                cursor.execute(sql,(course_id,section_id,))
                row = sql_util.dictfetchone(cursor)
                if row != None :
                    self._init_response()
                    res = {
                        'title':row['title'],
                        'course_id':row['course_id'],
                        'section_id':row['section_id'],
                        'dept_name':row['dept_name'],
                        'instructor_name':row['instructor_name'],
                        'credits':row['credits'],
                        'classroom_no':row['classroom_no'],
                        'day':row['day'],
                        'time':row['time'],
                        'lesson':row['lesson'],    
                    }
                    self.response.update(res)
                    return self._get_response(SEARCH_OK,1)
                else:
                    self._init_response()
                    return self._get_response(NO_RESULT,-1)

            if search_type == SEARCH_BY_NAME:
                title = self.data['title']
                sql = 'select * from section natural join course natural join teaches natural join instructor where title = %s'
                cursor.execute(sql,(title,))
                row = sql_util.dictfetchone(cursor)
                if row != None :
                    self._init_response()
                    res = {
                    'title':row['title'],
                    'course_id':row['course_id'],
                    'section_id':row['section_id'],
                    'dept_name':row['dept_name'],
                    'instructor_name':row['instructor_name'],
                    'credits':row['credits'],
                    'classroom_no':row['classroom_no'],
                    'day':row['day'],
                    'time':row['time'],
                    'lesson':row['lesson'],    
                    }
                    self.response.update(res)
                    return self._get_response(SEARCH_OK,1)
                else:
                    self._init_response()
                    return self._get_response(NO_RESULT,-1)

            if search_type == SEARCH_BY_DEPT:
                dept_name = self.data['dept_name']
                sql = 'select * from section natural join course natural join teaches natural join instructor where dept_name = %s'
                cursor.execute(sql,(dept_name,))
                rows = sql_util.dictfetchall(cursor)
                sections = []
                if rows != None :

                    for row in rows:
                        res = {
                            'title':row['title'],
                            'course_id':row['course_id'],
                            'section_id':row['section_id'],
                            'dept_name':row['dept_name'],
                            'instructor_name':row['instructor_name'],
                            'credits':row['credits'],
                            'classroom_no':row['classroom_no'],
                            'day':row['day'],
                            'time':row['time'],
                            'lesson':row['lesson'],    
                        }
                        sections.append(res)

                    self._init_response()
                    self.response.update(sections)
                    return self._get_response(SEARCH_OK,1)
                else:
                    self._init_response()
                    return self._get_response(NO_RESULT,-1)

            if search_type == SEARCH_BY_INSTRUCTOR:
                instructor_name = self.data['instructor_name']
                sql = 'select * from section natural join course natural join teaches natural join instructor where instructor_name = %s'
                cursor.execute(sql,(instructor_name,))
                rows = sql_util.dictfetchall(cursor)
                sections = []
                if rows != None :
                    for row in rows:
                        res = {
                            'title':row['title'],
                            'course_id':row['course_id'],
                            'section_id':row['section_id'],
                            'dept_name':row['dept_name'],
                            'instructor_name':row['instructor_name'],
                            'credits':row['credits'],
                            'classroom_no':row['classroom_no'],
                            'day':row['day'],
                            'time':row['time'],
                            'lesson':row['lesson'],    
                        }
                        sections.append(res)

                    self._init_response()
                    self.response.update(sections)
                    return self._get_response(SEARCH_OK,1)
                else:
                    self._init_response()
                    return self._get_response(NO_RESULT,-1)

                pass
            


        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

     