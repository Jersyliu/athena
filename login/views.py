from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login

from .models import NewUser, Course, Lesson, Progress, Challenge


def index(request):
    return render(request, 'login/index.html',{})

def dologin(request):
    username = request.POST['UserName']
    password = request.POST['PassWord']

    if len(username) > 30:
        return HttpResponseRedirect(reverse('login:index'))
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        a = NewUser.objects.get(username = username)
        request.session[a.username] = 1
        a.isOnline = True
        a.save()
        return HttpResponseRedirect(reverse('homepage:courseList',args = (request.POST["UserName"],)))
    else:
        return HttpResponseRedirect(reverse('login:index'))
    

    
def register(request):
    return render(request, 'login/register.html',{})


def doregister(request):
    try:
        user = NewUser.objects.get(username = request.POST["UserName"])
        return render(request, 'login/register.html',{"Already_exist":True,"Password_Not_Match":False})
    except NewUser.DoesNotExist:
        if len(request.POST["UserName"]) > 30:
            return HttpResponseRedirect(reverse('login:register'))
        for i in "/#?*+- ":
            if i in request.POST["UserName"]:
                return HttpResponseRedirect(reverse('login:register'))
        if request.POST["PassWord"] == request.POST["ConPassWord"]:
            user = NewUser.objects.create_user(username = request.POST["UserName"], password = request.POST["PassWord"])
            login(request, user)
            a = NewUser.objects.get(username = user.username)
            request.session[a.username] = 1
            a.isOnline = True
            a.save()
            return HttpResponseRedirect(reverse('homepage:courseList',args = (request.POST["UserName"],)))
        else:
            return render(request, 'login/register.html',{"Already_exist":False,"Password_Not_Match":True})
