import json
import traceback
from django.http import FileResponse,HttpResponse

from selectCourse.logs import logger
from selectCourse.util import sql_util
from django.db import connection
from selectCourse.constants.errorConstants import *
from selectCourse.constants.infoConstants import *

class DownloadService():

    def __init__(self,request):
        self.request = request
        self.response = {}
        if request.method == 'POST':
            self.data = request.POST

    def _init_response(self, status=None):
        if status and status["code"]:
            # self.response["result"] = False
            self.response["msg"] = status.get("msg", "")
            return
        elif status and status["code"] is None:
            self.response["msg"] = "invalid status"
            return
        self.response["msg"] = "success"

    def _get_response(self,msg=None,code=None):
        if msg != None:
            self.response["msg"] = msg
        if code != None:
            self.response["code"] = code
        return FileResponse(self.response)

    def execute(self):
        file_type = self.request.GET['file_type']
        if file_type == STUDENT_FILE:
            # file = open('/Users/huangjiani/CourseSelectionSystem/data/student_list_example.xlsx','rw')
            file = open('./select_service.py','rw')
            response = HttpResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="student_list_example.xlsx"'
            return response

        elif file_type == SECTION_FILE:
            file = open('../../data/section_list_example.xlsx','rw')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="section_list_example.xlsx"'
            return response

        elif file_type == SCORE_FILE:
            file = open('../../data/score_list_example.xlsx','rw')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="score_list_example.xlsx"'
            return response

        elif file_type == COURSE_FILE:
            file = open('../../data/course_list_example.xlsx','rw')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="course_list_example.xlsx"'
            return response

        elif file_type == INSTRUCTOR_FILE:
            file = open('../../data/instructor_list_example.xlsx','rw')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="instructor_list_example.xlsx"'
            return response





        

