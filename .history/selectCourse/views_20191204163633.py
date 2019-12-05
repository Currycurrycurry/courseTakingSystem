from django.shortcuts import render
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from selectCourse import models
import json


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def  write_server(request):
    data = json.loads(request.body)
    print(data)
    models.Classroom.objects.create(**data)
    res = {
        'success': True
    }
    return HttpResponse(json.dumps(res),content_type = 'application/json')


def read_server(request):
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


def login(self, request):
    res = {
        'code': 0,
        'msg': '',
        'data': {}
    }
    data = json.loads(request.body)
    print(data)
    print(models.Account.objects.all())
    user_id = data.get('id')
    pwd = request.data.get('password')

    try:
        user = models.Account.objects.get(id=user_id)
        if user.password == pwd:
            request.session['is_login'] = True
            request.session['user_id'] = user_id
            request.session['role'] = user.role
            request.session.set_expiry(0)
            res['msg'] = 'login successfully'
            res['code'] = 1
            res['data'] = {'username': user_id}
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
    # 0 - root 1 - students 2 -teachers
    if request.session['role'] == 1:
        course_id = request.GET['course_id']
        


        pass
    pass

def dropCourse(request):
    pass

# PAGE 3: for students to apply for courses
def applyCourse(request):
    pass

# PAGE 4: for students to check all his/her courses and the school courses
def checkCourseTable(request):
    pass

def checkAllCourses(request):
    pass

# PAGE 5: for students to check his/her own info
def checkPersonalInfo(request):
    pass
###################################################################################
# PAGE 6: for teachers to check the name list
def checkCourseNamelist(request):
    pass

# PAGE 7: for teachers to handle the course applications
def handleApplication(request):
    pass

# PAGE 8: for teachers to log the score of students in his class 
def registerScore(request):
    pass


# GET



