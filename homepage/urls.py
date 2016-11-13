from django.conf.urls import url

from . import views

app_name = "homepage"

urlpatterns = [
        url(r'course/(?P<username>[a-zA-Z0-9+]+)/(?P<coursename>[a-zA-Z0-9+]+)/(?P<lessonname>[ a-zA-Z0-9+]+)/$', views.course, name = 'course'),
        url(r'otherprofile/(?P<username>[a-zA-Z0-9+]+)/$', views.otherprofile, name = 'otherprofile'),
        url(r'profile/(?P<username>[a-zA-Z0-9+]+)/$', views.profile, name = 'profile'),
        url(r'logoutuser/$',views.logoutuser, name = 'logoutuser'),
        url(r'courselist/(?P<username>[a-zA-Z0-9+]+)/$', views.courseList, name = 'courseList'),  
]

