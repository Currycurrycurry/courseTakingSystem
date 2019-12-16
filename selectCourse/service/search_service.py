import json
import traceback
from django.http import JsonResponse

from selectCourse.logs import logger
from selectCourse.util import sql_util
from django.db import connection
from selectCourse.constants.errorConstants import *
from selectCourse.constants.infoConstants import *
from selectCourse.service.base_service import BaseService

# 2019.12.15 merge the checking all courses with searching courses.
class SearchService(BaseService):
    def __init__(self, request):
        super(SearchService, self).__init__(request)
        if request.method == 'POST':
            self.data = request.POST
        elif request.method == 'GET':
            self.data = request.GET

    def execute(self):
        if self.request.session['is_login'] != True:
            self._init_response()
            return self._get_response(UNAUTHORIZED,-1)

        try:
          
            course_id = self.data['course_id']
            section_id = self.data['section_id']
            title = self.data['title']
            instructor_name = self.data['instructor_name']
            dept_name = self.data['dept_name']
            page_num = self.data['page_num']

        except Exception as error:
            self._init_response()
            return self._get_response(GET_ARG_ERROR,-1)
        
        try:  
            get_dict = self.data.copy() 
            del get_dict['page_num']
            print(get_dict)
            cursor = connection.cursor()
            sql = 'select * from section natural join course natural join teaches natural join instructor'
            cnt_sql = 'select count(*) from section natural join course natural join teaches natural join instructor'
            sql_conditions = []
            for key in get_dict.keys():
                if get_dict[key]!=None and get_dict[key]!='':
                    sql_conditions.append(str(key+"='"+get_dict[key]+"'"))
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

            if rows != None:
                sections = []
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
                reses = {'sections':sections,
                            'total_num':total_num,}
                self.response.update(reses)
                return self._get_response(SEARCH_OK,1)
            else:
                self._init_response()
                return self._get_response(NO_RESULT,-1)

        except Exception as error:
            traceback.print_exc()
            connection.rollback()
            self._init_response()
            return self._get_response(SERVER_ERROR)

     