from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.contrib.auth import logout

from login.models import NewUser, Course, Lesson, Progress, Challenge


def profile(request, username):
    if request.user.is_authenticated:
        return render(request, 'homepage/profile.html',{"UserName":request.user.username})
    else:
        #return HttpResponseRedirect(reverse('login:index'))
        return render(request, 'homepage/logout.html')

def otherprofile(request, fromWho, toWho):
    return render(request, 'homepage/otherprofile.html',{"FromWhoName":fromWho,"ToWhoName":toWho})
    

def logoutuser(request):
    a = NewUser.objects.get(username = request.user.username)
    a.isOnline = False
    a.save()
    logout(request)
    return HttpResponseRedirect(reverse('login:index'))

def courseList(request, username):
    return render(request, 'homepage/courselist.html', {"CourseClass":Course.objects.all(),"User":request.user})
    
def course(request, username, coursename, lessonname):
    if coursename == lessonname:
        lesson = Lesson.objects.filter(course__course_name=coursename)[0]
    else:
        lesson = Lesson.objects.get(lesson_name=lessonname)
    whosOnline = NewUser.objects.filter(isOnline = True)
    context = {"CourseName": coursename,
               "User":request.user,
               "lessonDetail":Lesson.objects.filter(course__course_name=coursename),
               "loadlesson":lesson,
               "whosOnline":whosOnline
               }
    return render(request, 'homepage/course.html', context)

def challenge(request, username, coursename, lessonname, challengename):
    challenge = Lesson.objects.get(lesson_name=lessonname).challenge_set.get(challenge_name=challengename)
    whosOnline = NewUser.objects.filter(isOnline = True)
    context = {"CourseName": coursename,
               "User":request.user,
               "lessonDetail":Lesson.objects.filter(course__course_name=coursename),
               "loadlesson":challenge,
               "whosOnline":whosOnline
               }
    return render(request, 'homepage/course.html', context)
    
