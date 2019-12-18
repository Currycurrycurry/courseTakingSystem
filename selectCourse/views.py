from django.shortcuts import render
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from selectCourse import models
from django.db import connection
import json
import xlrd

from django.shortcuts import render
from django.views.decorators import csrf
##################################Constants#################################################
# AUTHORIZATION
ROOT_ROLE = 0
STUDENT_ROLE = 1
INSTRUCTOR_ROLE = 2

# APPLICATION STATUS
STATUS_PENDING = 0 # submitted successfully
STATUS_PASSED = 1
STATUS_UNPASSED = -1

# EXCEL FILE 
STUDENT_FILE = 1
COURSE_FILE = 2
SCORE_FILE = 3


##################################Index#################################################
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def test(request):
    ctx = {}
    return render(request, "test.html", ctx)


##################################Login in/out#################################################

def login_sql(request):
    res = {
        'code': 0,
        'msg': '',
        'data': {}
    }
    if request.method == "POST":
        data = request.POST
        print(data)
        user_id = data.get('id')
        pwd = data.get('password')
        res_user_name = ""

        try:
            cursor = connection.cursor()
            find_passwd_sql = "SELECT 'account'.'password', 'account'.'role' FROM 'account' WHERE 'account'.'id' = '"+user_id+"'"
            cursor.execute(find_passwd_sql)
            raw_pass = cursor.fetchone()
            print(raw_pass)
            if raw_pass == None:
                res['msg'] = 'wrong userid'
            else:
                if pwd == raw_pass[0]:
                    if STUDENT_ROLE == raw_pass[1]:
                        find_student_name_sql = "SELECT 'student'.'student_name' FROM 'student' WHERE 'student'.'student_id' = '"+user_id+"'"
                        cursor.execute(find_student_name_sql)
                        raw_student_name = cursor.fetchone()
                        print(raw_student_name)
                        res_user_name = raw_student_name[0]
                    if INSTRUCTOR_ROLE == raw_pass[1]:
                        find_instructor_name_sql = "SELECT 'instructor'.'instructor_name' FROM 'instructor' WHERE 'instructor'.'instructor_id' = '"+user_id+"'"
                        cursor.execute(find_instructor_name_sql)
                        raw_instructor_name = cursor.fetchone()
                        print(raw_instructor_name)
                        res_user_name = raw_instructor_name[0]
                    if ROOT_ROLE == raw_pass[1]:
                        res_user_name = "administrator"

                    request.session['is_login'] = True
                    request.session['user_name'] = res_user_name
                    request.session['user_id'] = user_id
                    request.session['role'] = raw_pass[1]
                    request.session.set_expiry(0)

                    res['msg'] = 'login successfully'
                    res['code'] = 1
                    res['data'] = {'user_id': user_id}
            
                else:
                    res['msg'] = 'wrong password' 
        except Exception as e:
            print(str(e))
        
        return HttpResponse(json.dumps(res),content_type = 'application/json')

    
# EVERY PAGE should have the logout button
def logout(request):
    request.session.flush()
    pass

##################################Select#################################################
# TODO 选课时间冲突检测 
# TODO 考试时间冲突检查
def select_sql(request):
    res = {
        'code': 0,
        'msg': ''
    }
    if request.session['is_login'] == True and request.session['role'] == STUDENT_ROLE:
        user_id = request.GET['user_id']
        course_id = request.GET['course_id']
        section_id = request.GET['section_id']
        print("the course id is ",course_id)
        print("the section id is ",section_id)

        cursor = connection.cursor()
        find_course_sql = "SELECT 'course'.'course_id' FROM 'course' WHERE 'course'.'course_id' ='"+course_id+"'"
        cursor.execute(find_course_sql)
        raw_course_id = cursor.fetchone()
        print("raw course id is ",raw_course_id)
        if raw_course_id == None:
            res['msg'] = 'wrong course id'
        else:
            find_section_sql = "SELECT * FROM 'section' WHERE 'section'.'course_id' ='"+course_id+"' AND 'section'.'section_id'="+section_id
            cursor.execute(find_section_sql)
            raw_section_info = cursor.fetchone()
            if raw_section_info == None:
                res['msg'] = 'wrong section id'
            else:
                find_whether_already_takes_sql = "SELECT * FROM 'takes' WHERE 'takes'.'course_id' = '"+course_id+"' AND 'takes'.'section_id' ="+section_id+" AND 'takes'.'student_id'='"+user_id+"'"
                cursor.execute(find_whether_already_takes_sql)
                raw_take_info = cursor.fetchone()
                print("raw take info is ",raw_take_info)
                if raw_take_info == None:
                    find_take_num_sql = "SELECT COUNT(*) FROM 'takes' WHERE 'takes'.'course_id' = '"+course_id+"' AND 'takes'.'section_id' ="+section_id
                    cursor.execute(find_take_num_sql)
                    raw_take_num = cursor.fetchone()
                    print("the take num is :",raw_take_num[0])
                    find_section_limit = "SELECT 'section'.'limit' FROM 'section' WHERE 'section'.'course_id'='"+course_id+"' AND 'section'.'section_id' ="+section_id
                    cursor.execute(find_section_limit)
                    raw_section_limit = cursor.fetchone()
                    print("the section limit is :",raw_section_limit[0])

                    if raw_section_limit[0] > raw_take_num[0]:
                        insert_takes_sql = "INSERT INTO 'takes' ('course_id','section_id','student_id','grade','drop_flag') SELECT '"+ course_id+"',"+section_id+",'"+user_id+"', NULL,0"
                        cursor.execute(insert_takes_sql)
                        check_credit_sql = "SELECT 'student'.'student_total_credit' FROM 'student' WHERE 'student'.'student_id' = '"+user_id+"'"
                        cursor.execute(check_credit_sql)
                        raw_credit = cursor.fetchone()
                        print("before update: the raw_credit is : ",raw_credit[0])
                        find_course_credit_sql = "SELECT 'course'.'credits' FROM 'course' WHERE 'course'.'course_id'='"+course_id+"'"
                        cursor.execute(find_course_credit_sql)
                        raw_course_credit = cursor.fetchone()
                        print("the course credit is ",raw_course_credit[0])
                        updated_credit = int(raw_credit[0]+raw_course_credit[0])
                        print("updated credit is",updated_credit)
                        add_credits_sql = "UPDATE 'student' SET 'student_total_credit'="+str(updated_credit)+" WHERE 'student'.'student_id'='"+user_id+"'"
                        cursor.execute(add_credits_sql)

                        res['msg'] = 'select successfully'
                        res['code'] = 1
                    else:
                        res['msg'] = 'course with no vacancy'

                else:
                    res['msg'] = 'already selected'
    else: 
        res['msg'] = 'unauthorized as student'

    return HttpResponse(json.dumps(res),content_type = 'application/json')

##################################Drop#################################################

def dropCourse_sql(request): 
    res = {
        'code': 0,
        'msg': ''
    }
    if request.session['is_login'] == True and request.session['role'] == STUDENT_ROLE:
        user_id = request.GET['user_id']
        course_id = request.GET['course_id']
        section_id = request.GET['section_id']
        print("the course id is ",course_id)
        print("the section id is ",section_id)

        cursor = connection.cursor()
        find_course_sql = "SELECT 'course'.'course_id' FROM 'course' WHERE 'course'.'course_id' ='"+course_id+"'"
        cursor.execute(find_course_sql)
        raw_course_id = cursor.fetchone()
        print("raw course id is ",raw_course_id)
        if raw_course_id == None:
            res['msg'] = 'wrong course id'
        else:
            find_section_sql = "SELECT * FROM 'section' WHERE 'section'.'course_id' ='"+course_id+"' AND 'section'.'section_id'="+section_id
            cursor.execute(find_section_sql)
            raw_section_info = cursor.fetchone()
            if raw_section_info == None:
                res['msg'] = 'wrong section id'
            else:
                find_whether_already_takes_sql = "SELECT * FROM 'takes' WHERE 'takes'.'course_id' = '"+course_id+"' AND 'takes'.'section_id' ="+section_id+" AND 'takes'.'student_id'='"+user_id+"'"
                cursor.execute(find_whether_already_takes_sql)
                raw_take_info = cursor.fetchone()
                print("raw take info is ",raw_take_info)
                if raw_take_info == None:
                    res['msg'] = 'drop error: haven\'t taken yet'
                else:
                    # drop couese
                    drop_course_sql = "DELETE FROM 'takes' WHERE ('takes'.'course_id' = '"+course_id+"' AND 'takes'.'section_id' ="+section_id+" AND 'takes'.'student_id' = '"+user_id+"')"
                    cursor.execute(drop_course_sql)

                    check_credit_sql = "SELECT 'student'.'student_total_credit' FROM 'student' WHERE 'student'.'student_id' = '"+user_id+"'"
                    cursor.execute(check_credit_sql)
                    raw_credit = cursor.fetchone()
                    print("before update: the raw_credit is : ",raw_credit[0])
                    find_course_credit_sql = "SELECT 'course'.'credits' FROM 'course' WHERE 'course'.'course_id'='"+course_id+"'"
                    cursor.execute(find_course_credit_sql)
                    raw_course_credit = cursor.fetchone()
                    print("the course credit is ",raw_course_credit[0])
                    updated_credit = int(raw_credit[0]-raw_course_credit[0])
                    print("updated credit is",updated_credit)
                    minus_credits_sql = "UPDATE 'student' SET 'student_total_credit'="+str(updated_credit)+" WHERE 'student'.'student_id'='"+user_id+"'"
                    cursor.execute(minus_credits_sql)
                    res['msg'] = 'drop successfully'
                    res['code'] = 1
    else: 
        res['msg'] = 'unauthorized as student'

    return HttpResponse(json.dumps(res),content_type = 'application/json')


##################################Check Infos#################################################
def checkCourseTable_sql(request):
    res = {
        'code': 0,
        'msg': '',
        'data':{}
    }

    if request.session['is_login'] == True and request.session['role'] == STUDENT_ROLE:
        user_id = request.GET['user_id']
        print("the user id is ",user_id)
        cursor = connection.cursor()
        check_courses_sql = "SELECT * FROM (SELECT * FROM 'section' NATURAL JOIN 'takes' WHERE 'takes'.'student_id'='"+user_id+"') NATUAL JOIN 'course' "
        cursor.execute(check_courses_sql)
        raw_courses_taken = cursor.fetchall()
        print("raw courses taken are :",raw_courses_taken)
        data = raw_courses_taken
        res['data'] = data
        res['code'] = 1
        res['msg'] = 'show course table'
     
    else: 
        res['msg'] = 'unauthorized as student'

    return HttpResponse(json.dumps(res),content_type = 'application/json')

# TODO: 加载过慢——ajax实现
def checkAllCourses_sql(request):
    res = {
        'code': 0,
        'msg': '',
        'data':{}
    }
    if request.session['is_login'] == True and request.session['role'] == STUDENT_ROLE:
        user_id = request.GET['user_id']
        print("the user id is ",user_id)
        cursor = connection.cursor()
        check_all_courses_sql = "SELECT * FROM 'section' NATUAL JOIN 'course'"
        cursor.execute(check_all_courses_sql)
        data = cursor.fetchall()
        res['data'] = data
        res['code'] = 1
        res['msg'] = 'show all courses '
     
    else: 
        res['msg'] = 'unauthorized as student'

    return HttpResponse(json.dumps(res),content_type = 'application/json')

def checkPersonalInfo_sql(request):
    res = {
        'code': 0,
        'msg': '',
        'data':{}
    }

    if request.session['is_login'] == True:
        user_id = request.GET['user_id']
        print("the user id is ",user_id)
        cursor = connection.cursor()
        if request.session['role'] == STUDENT_ROLE:
            check_personal_info_sql = "SELECT * FROM 'student' where 'student'.'student_id'='"+user_id+"'"
            cursor.execute(check_personal_info_sql)
            data = cursor.fetchone()
            # TODO check the score and calculate the total gpa 
            res['data'] = data
            res['code'] = 1
            res['msg'] = 'show student info '
        
        if request.session['role'] == INSTRUCTOR_ROLE:
            check_personal_info_sql = "SELECT * FROM 'instructor' where 'instructor'.'instructor_id'='"+user_id+"'"
            cursor.execute(check_personal_info_sql)
            data = cursor.fetchone()
            res['data'] = data
            res['code'] = 1
            res['msg'] = 'show instructor info '

    else: 
        res['msg'] = 'unauthorized'

    return HttpResponse(json.dumps(res,cls=DjangoJSONEncoder),content_type = 'application/json')

##################################Instructors: Check Course Name List#################################################
# PAGE 6: for teachers to check the name list
# PAY ATTENTION : have fixed the typo error in the table teaches (now  the instuctor_id be instructor_id )
def checkTaughtCourses_sql(request):
    res = {
        'code':0,
        'msg':'',
        'data':{}
    }
    if request.session['is_login'] == True and request.session['role'] == INSTRUCTOR_ROLE:
        user_id = request.GET['user_id']
        print("the user id is ",user_id)
        
        cursor = connection.cursor()
        check_courses_taught_sql ="SELECT * FROM (SELECT * FROM 'teaches' NATURAL JOIN 'section' WHERE 'teaches'.'instructor_id' = '"+user_id+"') NATURAL JOIN 'course' "
        cursor.execute(check_courses_taught_sql)
        data = cursor.fetchall()
        print("the courses taught are :",data)
        res['data'] = data
        res['code'] = 1
        res['msg'] = "show courses taught by the instructor"

    else:
        res['msg'] = 'unauthorized as instructor'
    return HttpResponse(json.dumps(res,cls=DjangoJSONEncoder),content_type = 'application/json')

def checkCourseNamelist_sql(request):
    res = {
        'code': 0,
        'msg': '',
        'data':{},
    }
    if request.session['is_login'] == True and request.session['role'] == INSTRUCTOR_ROLE:
        user_id = request.GET['user_id']
        print("the user id is ",user_id)
        course_id = request.GET['course_id']
        section_id = request.GET['section_id']
        print("the course id is",course_id)
        print("the section id is ",section_id)

        cursor = connection.cursor()
        check_namelist_sql = "SELECT * FROM 'takes' NATURAL JOIN 'student' WHERE 'takes'.'course_id'='"+course_id+"' AND 'takes'.'section_id'="+section_id
        cursor.execute(check_namelist_sql)
        data = cursor.fetchall()

        res['data'] = data
        res['code'] = 1
        res['msg'] = 'show all courses\' name list '
     
    else: 
        res['msg'] = 'unauthorized as instructor'

    return HttpResponse(json.dumps(res,cls=DjangoJSONEncoder),content_type = 'application/json')

####################Insturctors & Students :Application without enough test!###############################################################
# PAGE 7: for teachers to handle the course applications
def handleApplication_sql(request):
    res = {
        'code':0,
        'msg':'',
    }

    data = request.POST
    user_id = data.get("user_id") # PAY ATTENTION : it is the student user id!
    course_id = data.get("course_id")
    section_id = data.get("section_id")
    status = data.get("status")
    
    if request.session['is_login'] == True:
        if request.session['role'] == INSTRUCTOR_ROLE:
            # check all the applications whose course is under his/her management
            cursor = connection.cursor()
            handle_app_sql = "UPDATE application SET status = '"+status+"' WHERE student_id='"+user_id+"' AND course_id='"+course_id+"' AND section_id='"+section_id+"'"
            cursor.execute(handle_app_sql)
            raw_app_data = cursor.fetchall()
            res['code'] = 1
            res['msg'] = "handle successfully"

        else:
            res['msg'] = "unauthorized as instructor"
    else:
        res['msg'] = "unauthorized"

# TODO : according to the STATUS order the result
def checkApplication_sql(request):
    res = {
        'code':0,
        'msg':'',
        'data':{}
    }
    user_id = request.GET['user_id']

    if request.session['is_login'] == True:
        if request.session['role'] == INSTRUCTOR_ROLE:
            # check all the applications whose course is under his/her management
            cursor = connection.cursor()
            find_target_apps_sql = "SELECT * FROM teaches NATURAL JOIN application WHERE instructor_id='"+user_id+"'"
            cursor.execute(find_target_apps_sql)
            raw_app_data = cursor.fetchall()
            res['code'] = 1
            res['msg'] = "check application info"
            res['data'] = raw_app_data
        elif request.session['role'] == STUDENT_ROLE:
            # check all the applications whose course is under his/her management
            cursor = connection.cursor()
            find_target_apps_sql = "SELECT * FROM student NATURAL JOIN application WHERE student_id='"+user_id+"'"
            cursor.execute(find_target_apps_sql)
            raw_app_data = cursor.fetchall()
            res['code'] = 1
            res['msg'] = "check application info"
            res['data'] = raw_app_data
        else:
            res['msg'] = "unauthorized as instructor"

    else:
        res['msg'] = "unauthorized"

# PAGE 3: for students to apply for courses
# can't apply selected courses 
# can't apply courses with vacancy
# can't apply dropped courses
# can't apply courses whose selected number will be  greater than the classroom capacity
# one student for one section can apply for one time
def applyCourse_sql(request):
# RESTRICTION: can't apply the courses which have been applied before but dropped (drop flag = 1)
    res = {
        'code': 0,
        'msg': '',
    }

    # 0 - root 1 - students 2 -teachers
    if request.session['is_login'] == True:
        # user_id = request.GET['user_id']
        # print("the user id is ",user_id)
        cursor = connection.cursor()
        if request.session['role'] == STUDENT_ROLE:
            # since the total data amount is big, use the post method.
            data = request.POST
            print(data)
            user_id = data.get('user_id')
            course_id = data.get('course_id')
            section_id = data.get('section_id')
            app_reason = data.get('application_reason')
    
            find_whether_already_applys_sql = "SELECT * FROM 'application' WHERE 'application'.'course_id' = '"+course_id+"' AND 'application'.'section_id' ="+section_id+" AND 'application'.'student_id'='"+user_id+"'"
            cursor.execute(find_whether_already_applys_sql)
            raw_apply_info = cursor.fetchone()
            print("raw take info is ",raw_apply_info)
            if raw_apply_info == None:
                find_whether_already_takes_sql = "SELECT * FROM 'takes' WHERE 'takes'.'course_id' = '"+course_id+"' AND 'takes'.'section_id' ="+section_id+" AND 'takes'.'student_id'='"+user_id+"'"
                cursor.execute(find_whether_already_takes_sql)
                raw_take_info = cursor.fetchone()
                print("raw take info is ",raw_take_info)
                if raw_take_info == None:
                    find_take_num_sql = "SELECT COUNT(*) FROM 'takes' WHERE 'takes'.'course_id' = '"+course_id+"' AND 'takes'.'section_id' ="+section_id
                    cursor.execute(find_take_num_sql)
                    raw_take_num = cursor.fetchone()
                    print("the take num is :",raw_take_num[0])
                    find_section_limit = "SELECT 'section'.'limit' FROM 'section' WHERE 'section'.'course_id'='"+course_id+"' AND 'section'.'section_id' ="+section_id
                    cursor.execute(find_section_limit)
                    raw_section_limit = cursor.fetchone()
                    print("the section limit is :",raw_section_limit[0])

                    find_section_capacity = "SELECT capacity FROM classroom NATURAL JOIN section WHERE course_id='"+course_id+"' AND section_id='"+section_id+"'"
                    cursor.execute(find_section_capacity)
                    raw_section_capacity = cursor.fetchone()
                    print("the section capacity is ",raw_section_capacity[0])
                    
                    if raw_section_limit[0] > raw_take_num[0]:
                        res['msg'] = "can't apply course with vacancy"
                    elif raw_take_num[0] >= raw_section_capacity[0] :
                        res['msg'] = "exceed the classroom capacity"
                    else:
                        check_drop_flag_app_sql = "SELECT 'application'.'if_drop' FROM 'application' WHERE 'application'.'course_id'='"+course_id+"' AND 'application'.'section_id'='"+section_id+"' AND 'application'.'student_id'='"+user_id+"'"
                        cursor.execute(check_drop_flag_app_sql)
                        raw_whether_drop = cursor.fetchone()
                        if raw_whether_drop == None or raw_whether_drop[0] == 0:
                            # insert_takes_sql = "INSERT INTO 'takes' ('course_id','section_id','student_id','grade','drop_flag') SELECT '"+ course_id+"',"+section_id+",'"+user_id+"', NULL,0"
                            # without application id, so maybe buggy
                            apply_course_sql = "INSERT INTO 'application' ('course_id','section_id','student_id','status','application_reason') SELECT '"+course_id+"',"+section_id+",'"+user_id+"',0,'"+app_reason+"'"
                            cursor.execute(apply_course_sql)
                            res['code'] = 1
                            res['msg'] = "apply successfully"
                        else:
                            res['msg'] = "can't apply dropped course"
                else:
                    res['msg'] = "can't apply selected course"
            else:
                res['msg'] = "can't apply course which is already applied"
        else: 
            res['msg'] = "unauthorized as student"
    else: 
        res['msg'] = 'unauthorized'

    return HttpResponse(json.dumps(res,cls=DjangoJSONEncoder),content_type = 'application/json')

#############################Uploading and Excel Processing###############################################################
# PAGE 8: for teachers to log the score of students in his class 
def importExcel(res,request):
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

# judge the inserted excel whether have duplicate student list 
# TODO change the score into grade when registering
def registerScore_sql(request):
    res = {
        'code': 0,
        'msg': '',
    }

    raw_student_scores = importExcel(res,request)
    print("the student scores are ",raw_student_scores)

# Auto import student info
def registerStudent_sql(request):
    res = {
        'code': 0,
        'msg': '',
    }
    raw_student_infos = importExcel(res,request)
    print("the raw student infos are ",raw_student_infos)

# Auto import instructor info
def registerInstructor_sql(request):
    res = {
        'code': 0,
        'msg': '',
    }
    raw_instructor_infos = importExcel(res,request)
    print("the raw instructor infos are ",raw_instructor_infos)

# Auto import course info 
# Tables need to insert : course section exam 
def registerCourses_sql(request):
    res = {
        'code': 0,
        'msg': '',
    }
    raw_course_infos = importExcel(res,request)
    print("the raw course infos are ",raw_course_infos)


#######################################Search###############################################################
# according to what to search? : (1) instructor (2) course_id+section_id (3) dept_name
def searchCourse_sql(request):

    pass


######################################Exam Info#############################################################
def checkExamInfo(request):

    pass


######################################Download Template File#################################################
from django.http import FileResponse
def download_template_file(request):
    file_type = request.GET('file_type')
    if file_type == STUDENT_FILE:
        file = open('../data/student_list_example.xlsx','rw')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="student_list_example.xlsx"'
        return response

    elif file_type == COURSE_FILE:
        file = open('../data/course_list_example.xlsx','rw')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="course_list_example.xlsx"'
        return response

    elif file_type == SCORE_FILE:
        file = open('../data/score_list_example.xlsx','rw')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="score_list_example.xlsx"'
        return response






