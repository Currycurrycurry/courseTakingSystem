from django.http import HttpResponse
from django.shortcuts import render
 
def hello(request):
    # return HttpResponse("Hello world ! ")
    context = {}
    context['hello'] = '123123123!'
    return render(request,'index.html',context) #使用模版输出数据，实现数据与视图分离
