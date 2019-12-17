from django.shortcuts import render
from django.views.decorators import csrf


def login_view(request):
    ctx = {}
    return render(request, "login.html", ctx)


def index(request):
    ctx = {}
    return render(request, "index.html", ctx)



