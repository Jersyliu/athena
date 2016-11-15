from django.conf.urls import url

from . import views

app_name = "homepage"

urlpatterns = [
        url(r'course/(?P<username>[^/]+)/(?P<coursename>[^/]+)/(?P<lessonname>[^/]+)/$', views.course, name = 'course'),
        url(r'otherprofile/(?P<fromWho>[^/]+)/(?P<toWho>[^/]+)/$', views.otherprofile, name = 'otherprofile'),
        url(r'profile/(?P<username>[^/]+)/$', views.profile, name = 'profile'),
        url(r'logoutuser/$',views.logoutuser, name = 'logoutuser'),
        url(r'courselist/(?P<username>[^/]+)/$', views.courseList, name = 'courseList'),  
]

