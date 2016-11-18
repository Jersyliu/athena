from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.contrib.auth import logout

from login.models import NewUser, Course, Lesson, Progress, Challenge, ChallengeProgress, CourseLocation


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
    p = Progress.objects.filter(newuser__username=username, lesson__lesson_name=lessonname)
    if len(p) == 0:
        Text = ""
    else:
        Text = p[0].progress_until_now
    context = {"CourseName": coursename,
               "User":request.user,
               "lessonDetail":Lesson.objects.filter(course__course_name=coursename),
               "loadlesson":lesson,
               "whosOnline":whosOnline,
               "isLesson": "true",
               "Text":Text
               }
    return render(request, 'homepage/course.html', context)

def challenge(request, username, coursename, lessonname, challengename):
    challenge = Lesson.objects.get(lesson_name=lessonname).challenge_set.get(challenge_name=challengename)
    whosOnline = NewUser.objects.filter(isOnline = True)
    p = ChallengeProgress.objects.filter(newuser__username=username, challenge__challenge_name=challengename)
    if len(p) == 0:
        Text = ""
    else:
        Text = p[0].progress_until_now
    context = {"CourseName": coursename,
               "User":request.user,
               "lessonDetail":Lesson.objects.filter(course__course_name=coursename),
               "loadlesson":challenge,
               "whosOnline":whosOnline,
               "isLesson": "false",
               "Text":Text
               }
    return render(request, 'homepage/course.html', context)

def keepprogress(request, username, lessonname):
    #NewUser.objects.create_user(username="OPP", password="123")
    #isLesson = "true"
    if request.POST["haha"] == "true":
        a = Progress.objects.filter(newuser__username = username, lesson__lesson_name = lessonname)
        if len(a) == 0:
            p = Progress(newuser=NewUser.objects.get(username=username), lesson=Lesson.objects.get(lesson_name=lessonname), progress_until_now=request.POST["inputcode"])
            p.save()
        else:
            p = Progress.objects.get(newuser__username = username, lesson__lesson_name = lessonname)
            p.progress_until_now = request.POST["inputcode"]
            p.save()
        if request.POST["isC"] == True:
            p.is_complete = True
            p.save()
        return HttpResponse("")
    else:
        #return HttpResponse("jlskdjf")
        a = ChallengeProgress.objects.filter(newuser__username = username, challenge__challenge_name = lessonname)
        #return HttpResponse("jlskdjf")
        if len(a) == 0:
            #return HttpResponse("jlskdjf")
            p = ChallengeProgress(newuser=NewUser.objects.get(username=username), challenge=Challenge.objects.get(challenge_name=lessonname), progress_until_now=request.POST["inputcode"])
            p.save()
            #return HttpResponse("jlskdjf")
        else:
            p = ChallengeProgress.objects.get(newuser__username = username, challenge__challenge_name = lessonname)
            p.progress_until_now = request.POST["inputcode"]
            p.save()
        if request.POST["isC"] == True:
            p.is_complete = True
            p.save()
        return HttpResponse("")
        
