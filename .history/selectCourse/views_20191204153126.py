from django.shortcuts import render
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder


# add for login
# from rest_framework.viewsets import ModelViewSet
# from .serializers import UserSerializer, User
# from rest_framework.decorators import action
# from django.contrib.auth import login
# from rest_framework.response import Response

# Create your views here.
from django.http import HttpResponse
from selectCourse import models
import json
# import uuid



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
# POST write to server
# PAGE 1 : for login 
# Suppose the models.User has been added 
# All that can been done by the frontend will be ignored in it.


# class UserViewset(ModelViewSet):
   
    # serializer_class = UserSerializer
# queryset = Acount.objects.all()

    # @action(methods=['POST'], url_path='login', detail=False)

def login(self, request):

    user_id = request.data.get('id')
    pwd = request.data.get('password')

    res = {
        'code': 0,
        'msg': '',
        'data': {}
    }
    if not all([id, pwd]):
        res['msg'] = 'wrong parameter'
        return HttpResponse(json.dumps(res),content_type = 'application/json')
    print(request.data)
    try:
        user = models.Acount.objects.get(id=user_id, password=pwd)
    except:
        res['msg'] = 'wrong userid or wrong password'
        return HttpResponse(json.dumps(res),content_type = 'application/json')

    # if user.is_active != 1:
    #     res['msg'] = '用户不可用，请重新登陆。'
    #     return HttpResponse(json.dumps(res),content_type = 'application/json')

    request.session['login'] = True
    request.session['FS_YWPT'] = True
    request.session.set_expiry(0)
    res['msg'] = 'login successfully'
    res['code'] = 1
    res['data'] = {'username': user_id}
    return HttpResponse(json.dumps(res),content_type = 'application/json')

# def login(request):
#     if  
    
#     pass

# EVERY PAGE should have the logout button
def logout(request):
    pass

# PAGE 2: for students to select and drop courses (2&4 can be merged to one page)
def selectCourse(request):
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

