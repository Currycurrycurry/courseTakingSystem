from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from selectCourse import models
import json
# import uuid

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def  write_server(request):
    data = json.loads(request.body)
    print(data)
    # data['id'] = uuid.uuid4()
    models.Classroom.objects.create(**data)
    res = {
        'success': True
    }
    return HttpResponse(json.dump(res),content_type = 'application/json')

def read_server(request):
    classroom_no = request.GET['classroom_no']
    data = serializers.serialize('python',models.Classroom.objects.filter(classroom_no=classroom_no))
    res={
        'success':True,
        'data':data
    }
    return HttpResponse(json.dumps(res,cls=DjangoJSONEncoder),content_type='application/json')

