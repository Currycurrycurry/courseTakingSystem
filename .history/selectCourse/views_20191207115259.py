from django.shortcuts import render
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from selectCourse import models
import json

ROOT_ROLE = 0
STUDENT_ROLE = 1
INSTRUCTOR_ROLE = 2


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def  write_server(request):
    # data = json.loads(request.body)
    data = request.POST
    print(data)
    # models.Classroom.objects.create(**data)
    res = {
        'success': True
    }
    return HttpResponse(json.dumps(res),content_type = 'application/json')


def read_server(request):
    print(request.GET)
    number = request.GET['classroom_no']
    print(number)
    print(models.Classroom.objects.all())
    data = serializers.serialize('python',models.Classroom.objects.filter(classroom_no=number))
    print(data) #from obj to json
    res={
        'success':True,
        'data':data
    }
    return HttpResponse(json.dumps(res,cls=DjangoJSONEncoder),content_type='application/json')


def login(request):
    res = {
        'code': 0,
        'msg': '',
        'data': {}
    }
    if request.method == "POST":
        data = request.POST
        print(data)
        print(models.Account.objects.all())
        user_id = data.get('id')
        pwd = data.get('password')

        try:
            user = models.Account.objects.get(id=user_id)
            if user.password == pwd:

                student = models.Student.objects.get(student_id=user_id)
                # other required values to be added in the session
                request.session['is_login'] = True
                request.session['user_name'] = student.student_name
                request.session['role'] = user.role
                request.session.set_expiry(0)

                res['msg'] = 'login successfully'
                res['code'] = 1
                res['data'] = {'user_id': user_id}
            else:
                res['msg'] = 'wrong password'
        except:
            res['msg'] = 'wrong userid'
        
        return HttpResponse(json.dumps(res),content_type = 'application/json')

    
# EVERY PAGE should have the logout button
def logout(request):
    request.session.flush()
    pass

# PAGE 2: for students to select and drop courses (2&4 can be merged to one page)
def selectCourse(request):
    res = {
        'code': 0,
        'msg': ''
    }
    # 0 - root 1 - students 2 -teachers
    if request.session['is_login'] == True and request.session['role'] == STUDENT_ROLE:
        user_id = request.GET['user_id']
        course_id = request.GET['course_id']
        print("the course id is ",course_id)

        try:
            course = models.Course.objects.get(course_id=course_id)
            print("course is ",course)
            section = models.Section.objects.get(course=course)
            print("section is ",section)
            student = models.Student.objects.get(student_id=user_id)
            print("student is ",student)
            take_num = models.Takes.objects.filter(course_id=course_id).count()
            print(take_num)
            models.Takes.objects.create(course_id=course.course_id,section_id=section.section_id,student=student)
            # not quite sure if student=student is ok
            if models.Takes.objects.filter(course_id=course_id,student=student):
                res['msg'] = 'already selected'
            elif take_num < section.limit:
                pass
                #  INSERT INTO "takes" ("course_id", "section_id", "student_id", "grade", "drop_flag") SELECT 'XDSY118020', 1, '17302010015', NULL, NULL; args=('XDSY118020', 1, '17302010015', None, None)
                # models.Takes.objects.create(course_id=course.course_id,section_id=section.section_id,student=student)
                # models.Student.objects.filter(student_id=user_id).update(student_total_credit=student_total_credit+course.credits) # maybe buggy
                # use the save() method to update the credit
                # student.student_total_credit += course.credits
                # student.save()
                # res['msg'] = 'select successfully'
                # res['code'] = 1
            else:
                res['msg'] = 'course with no vacancy'
            
        except:
            res['msg'] = 'wrong course id'
    else: 
        res['msg'] = 'unauthorized as student'

    return HttpResponse(json.dumps(res),content_type = 'application/json')

def dropCourse(request):
    res = {
        'code': 0,
        'msg': ''
    }
    # 0 - root 1 - students 2 -teachers
    if request.session['is_login'] == TRUE and request.session['role'] == STUDENT_ROLE:
        user_id = request.GET['user_id']
        course_id = request.GET['course_id']
        print("the course id is ",course_id)

        try:
            course = models.Course.objects.get(course_id=course_id)
            section = models.Section.objects.get(course=course)
            student = models.Student.objects.get(student_id=user_id)
            take_num = models.Takes.objects.filter(course_id=course_id).count()
            # not quite sure if student=student is ok
            if models.Takes.objects.filter(course_id=course_id,student=student):
                models.Takes.objects.filter(course_id=course_id,student=student).delete()
                models.Student.objects.filter(student_id=user_id).update(student_total_credit=student_total_credit-course.credits) # maybe buggy
                res['msg'] = 'drop successfully'
                res['code'] = 1

            else:
                res['msg'] = 'drop error: haven\'t taken yet' 
        except:
            res['msg'] = 'wrong course id'
    else: 
        res['msg'] = 'unauthorized as student'

    return HttpResponse(json.dumps(res),content_type = 'application/json')
    

# PAGE 4: for students to check all his/her courses and the school courses
def checkCourseTable(request):
    res = {
        'code': 0,
        'msg': '',
        'data':{}
    }
    # 0 - root 1 - students 2 -teachers
    if request.session['is_login'] == TRUE and request.session['role'] == STUDENT_ROLE:
        user_id = request.GET['user_id']
        print("the user id is ",course_id)

        student = models.Student.objects.get(student_id=user_id)
        courses = models.Takes.objects.filter(student=student)
        data = serializers.serialize('python',models.Takes.objects.filter(student=student))
        res['data'] = data
        res['code'] = 1
        res['msg'] = 'show course table'
     
    else: 
        res['msg'] = 'unauthorized as student'

    return HttpResponse(json.dumps(res,cls=DjangoJSONEncoder),content_type = 'application/json')

    pass

# need to paginate
def checkAllCourses(request):
    res = {
        'code': 0,
        'msg': '',
        'data':{}
    }
    # 0 - root 1 - students 2 -teachers
    if request.session['is_login'] == TRUE and request.session['role'] == STUDENT_ROLE:
        user_id = request.GET['user_id']
        print("the user id is ",course_id)

        data = serializers.serialize('python',models.Section.objects.all())
        res['data'] = data
        res['code'] = 1
        res['msg'] = 'show all courses '
     
    else: 
        res['msg'] = 'unauthorized as student'

    return HttpResponse(json.dumps(res,cls=DjangoJSONEncoder),content_type = 'application/json')


# PAGE 5: for students to check his/her own info
def checkPersonalInfo(request):
    res = {
        'code': 0,
        'msg': '',
        'data':{}
    }

    # 0 - root 1 - students 2 -teachers
    if request.session['is_login'] == TRUE and request.session['role'] == STUDENT_ROLE:
        user_id = request.GET['user_id']
        print("the user id is ",course_id)

        data = serializers.serialize('python',models.Student.objects.filter(student_id=user_id))
        res['data'] = data
        res['code'] = 1
        res['msg'] = 'show student info '
     
    else: 
        res['msg'] = 'unauthorized as student'

    return HttpResponse(json.dumps(res,cls=DjangoJSONEncoder),content_type = 'application/json')


###################################################################################
# PAGE 6: for teachers to check the name list
def checkCourseNamelist(request):
    res = {
        'code': 0,
        'msg': '',
        'data':{},
        'course_num':0
    }
    # 0 - root 1 - students 2 -teachers
    if request.session['is_login'] == TRUE and request.session['role'] == INSTRUCTOR_ROLE:
        user_id = request.GET['user_id']
        print("the user id is ",course_id)

        instructor = models.Instructor.objects.get(instructor_id=user_id)
        courses = models.Teaches.objects.filter(instructor=instructor)
        courses = [x.course_id for x in courses ]
        res['course_num'] = len(courses)
        data = {}
        for course_id in courses:
            students_taken = models.Takes.objects.filter(course_id=course_id).values('student')
            data[course_id] = students_taken # maybe buggy
            
        data = serializers.serialize('python',models.Teaches.objects.filter(instructor=instructor))
        res['data'] = data
        res['code'] = 1
        res['msg'] = 'show all courses\' name list '
     
    else: 
        res['msg'] = 'unauthorized as instructor'

    return HttpResponse(json.dumps(res,cls=DjangoJSONEncoder),content_type = 'application/json')

    
# PAGE 7: for teachers to handle the course applications
def handleApplication(request):
    pass


# PAGE 3: for students to apply for courses
def applyCourse(request):
    pass

# PAGE 8: for teachers to log the score of students in his class 
def registerScore(request):
    pass


# GET



