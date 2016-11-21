from django.conf.urls import url

from . import views

app_name = "homepage"

urlpatterns = [
        url(r'keepnotes/(?P<username>[^/]+)/(?P<lessonname>[^/]+)/$', views.keepnotes, name = 'keepnotes'),
        url(r'chat/(?P<fromID>[^/]+)/(?P<fromName>[^/]+)/(?P<toID>[^/]+)/(?P<toName>[^/]+)$', views.chat, name = 'chat'),
        url(r'keepprogress/(?P<username>[^/]+)/(?P<lessonname>[^/]+)/$', views.keepprogress, name = 'keepprogress'),
        url(r'course/(?P<username>[^/]+)/(?P<coursename>[^/]+)/(?P<lessonname>[^/]+)/$', views.course, name = 'course'),
        url(r'otherprofile/(?P<fromWho>[^/]+)/(?P<toWho>[^/]+)/$', views.otherprofile, name = 'otherprofile'),
        url(r'profile/(?P<username>[^/]+)/$', views.profile, name = 'profile'),
        url(r'logoutuser/$',views.logoutuser, name = 'logoutuser'),
        url(r'courselist/(?P<username>[^/]+)/$', views.courseList, name = 'courseList'),
        url(r'challenge/(?P<username>[^/]+)/(?P<coursename>[^/]+)/(?P<lessonname>[^/]+)/(?P<challengename>[^/]+)$', views.challenge, name = 'challenge')
]

