from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.utils import timezone

from login.models import NewUser, Course, Lesson, Progress, Challenge, ChallengeProgress, CourseLocation

from random import shuffle
def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return NewUser.objects.filter(id__in=uid_list)



def profile(request, username):
    if request.user.is_authenticated:
        context = {
            "UserName":request.user.username,
            "Progress":Progress.objects.filter(newuser__username=username),
            "CProgress":ChallengeProgress.objects.filter(newuser__username=username),
            "score": NewUser.objects.get(username=username).score,
            "picture": NewUser.objects.get(username=username).picture
            }
        return render(request, 'homepage/profile.html',context)
    else:
        #return HttpResponseRedirect(reverse('login:index'))
        return render(request, 'homepage/logout.html')

def otherprofile(request, fromWho, toWho):
    context = {
        "ToWhoName":toWho,
        "Progress":Progress.objects.filter(newuser__username=toWho),
        "CProgress":ChallengeProgress.objects.filter(newuser__username=toWho),
        "FromWhoName":fromWho
        }
    return render(request, 'homepage/otherprofile.html', context)
    

def logoutuser(request):
    a = NewUser.objects.get(username = request.user.username)
    a.isOnline = False
    a.save()
    logout(request)
    return HttpResponseRedirect(reverse('login:index'))

def courseList(request, username):
    whosOnline = get_all_logged_in_users()
    lessonP10 = Progress.objects.filter(is_complete=True)
    challengeP10 = ChallengeProgress.objects.filter(is_complete=True)
    news = []
    for i in lessonP10:
        news.append(i)
    for i in challengeP10:
        news.append(i)
    shuffle(news)
    easy = Course.objects.filter(level="easy")
    medium = Course.objects.filter(level="medium")
    hard = Course.objects.filter(level="hard")
    context = {
           "User":request.user,
           "CourseClass":Course.objects.all(),
           "easy":easy,
           "medium":medium,
           "hard":hard,
           "whosOnline":whosOnline,
           "picture": NewUser.objects.get(username=username).picture,
           "score": NewUser.objects.get(username=username).score,
           "news":news
           }
    return render(request, 'homepage/courselist.html', context )
    
def course(request, username, coursename, lessonname):
    CL = CourseLocation.objects.filter(newuser__username=username, course__course_name=coursename)
    l = Lesson.objects.filter(lesson_name=lessonname)
    if len(CL) == 0:
        lesson = Lesson.objects.filter(course__course_name=coursename)[0]
        cl = CourseLocation(newuser=NewUser.objects.get(username=username), course=Course.objects.get(course_name=coursename), islessonornot=True, whichone=lesson.lesson_name)
        cl.save()
    elif CL[0].islessonornot == False and len(l) == 0:
        return HttpResponseRedirect(reverse('homepage:challenge',args=(username,coursename,lessonname,CL[0].whichone)))
    else:
#        cl = CourseLocation.objects.get(newuser__username=username, course__course_name=coursename)
        cl = CL[0]
        if coursename == lessonname:
            lesson = Lesson.objects.get(lesson_name=cl.whichone)
        else:
            lesson = Lesson.objects.get(lesson_name=lessonname)
            cl.whichone = lesson.lesson_name
            cl.islessonornot = True
            cl.save()
    '''
    if coursename == lessonname:
        lesson = Lesson.objects.filter(course__course_name=coursename)[0]
    else:
        lesson = Lesson.objects.get(lesson_name=lessonname)
    '''
    #whosOnline = NewUser.objects.filter(isOnline = True)
    '''
    whosOnline = []
    alluser = NewUser.objects.all()
    for i in alluser:
        if i.username in request.session:
            whosOnline.append(NewUser.objects.get(username = i.username))
    '''
    whosOnline = get_all_logged_in_users()


    p = Progress.objects.filter(newuser__username=username, lesson__lesson_name=lessonname)
    if len(p) == 0:
        Text = ""
        TextNotes = ""
    else:
        Text = p[0].progress_until_now
        TextNotes = p[0].notes
    completeprogresses = Progress.objects.filter(newuser__username=username, is_complete=True)
    completeLesson = [i.lesson for i in completeprogresses]
    completeCprogresses = ChallengeProgress.objects.filter(newuser__username=username, is_complete=True)
    completeChallenges = [i.challenge for i in completeCprogresses]
    context = {"CourseName": coursename,
               "User":request.user,
               "lessonDetail":Lesson.objects.filter(course__course_name=coursename),
               "loadlesson":lesson,
               "name":lesson.lesson_name,
               "whosOnline":whosOnline,
               "isLesson": "true",
               "Text":Text,
               "TextNotes":TextNotes,
               "progress": completeLesson,
               "cprog": completeChallenges,
               "picture": NewUser.objects.get(username=username).picture,
               "score": NewUser.objects.get(username=username).score
               }
    return render(request, 'homepage/course.html', context)

def challenge(request, username, coursename, lessonname, challengename):
    challenge = Challenge.objects.get(challenge_name=challengename)
    cl = CourseLocation.objects.get(newuser__username=username, course__course_name=coursename)
    cl.whichone = challenge.challenge_name
    cl.islessonornot = False
    cl.save()
    #whosOnline = NewUser.objects.filter(isOnline = True)
    '''
    whosOnline = []
    alluser = NewUser.objects.all()
    for i in alluser:
        if i.username in request.session:
            whosOnline.append(NewUser.objects.get(username = i.username))
    '''
    whosOnline = get_all_logged_in_users()

    
    p = ChallengeProgress.objects.filter(newuser__username=username, challenge__challenge_name=challengename)
    if len(p) == 0:
        Text = ""
        TextNotes = ""
    else:
        Text = p[0].progress_until_now
        TextNotes = p[0].notes
        
    completeprogresses = Progress.objects.filter(newuser__username=username, is_complete=True)
    completeLesson = [i.lesson for i in completeprogresses]
    completeCprogresses = ChallengeProgress.objects.filter(newuser__username=username, is_complete=True)
    completeChallenges = [i.challenge for i in completeCprogresses]
    context = {"CourseName": coursename,
               "User":request.user,
               "lessonDetail":Lesson.objects.filter(course__course_name=coursename),
               "loadlesson":challenge,
               "name":challenge.challenge_name,
               "whosOnline":whosOnline,
               "isLesson": "false",
               "Text":Text,
               "TextNotes":TextNotes,
               "progress": completeLesson,
               "cprog": completeChallenges,
               "picture": NewUser.objects.get(username=username).picture,
               "score": NewUser.objects.get(username=username).score
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
        if request.POST["isC"] == "true":
            if p.is_complete == False:
                u = NewUser.objects.get(username=username)
                u.score += p.lesson.point_value
                u.save()
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
        if request.POST["isC"] == "true":
            if p.is_complete == False:
                u = NewUser.objects.get(username=username)
                u.score += p.challenge.point_value
                u.save()
            p.is_complete = True
            p.save()
        return HttpResponse("")
        
        
def keepnotes(request, username, lessonname):
    if request.POST["haha"] == "true":
        a = Progress.objects.filter(newuser__username = username, lesson__lesson_name = lessonname)
        if len(a) == 0:
            p = Progress(newuser=NewUser.objects.get(username=username), lesson=Lesson.objects.get(lesson_name=lessonname), notes=request.POST["notes"])
            p.save()
        else:
            p = Progress.objects.get(newuser__username = username, lesson__lesson_name = lessonname)
            p.notes=request.POST["notes"]
            p.save()
        return HttpResponse("")
    else:
        a = ChallengeProgress.objects.filter(newuser__username = username, challenge__challenge_name = lessonname)
        if len(a) == 0:
            p = ChallengeProgress(newuser=NewUser.objects.get(username=username), challenge=Challenge.objects.get(challenge_name=lessonname), notes=request.POST["notes"])
            p.save()
        else:
            p = ChallengeProgress.objects.get(newuser__username = username, challenge__challenge_name = lessonname)
            p.notes=request.POST["notes"]
            p.save()
        return HttpResponse("")


def chat(request, fromID, fromName, toID, toName):
    context = {
        "fromID": fromID,
        "fromName": str(fromName),
        "toID": toID,
        "toName": toName
        }
    return render(request, 'homepage/chat/fullview.html', context)
