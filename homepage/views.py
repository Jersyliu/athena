from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.contrib.auth import logout

from login.models import NewUser, Course, Lesson, Progress


def profile(request, username):
    if request.user.is_authenticated:
        return render(request, 'homepage/profile.html',{"UserName":request.user.username})
    else:
        #return HttpResponseRedirect(reverse('login:index'))
        return render(request, 'homepage/logout.html')
    

def logoutuser(request):
    logout(request)
    return HttpResponseRedirect(reverse('login:index'))

def courseList(request, username):
    return render(request, 'homepage/courselist.html', {"CourseClass":Course.objects.all(),"User":request.user})
    
def course(request, username, coursename):
    return render(request, 'homepage/course.html', {"CourseName": coursename, "User":request.user, "lessonDetail":Lesson.objects.filter(course__course_name=coursename)})
