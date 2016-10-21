from django.conf.urls import url

from . import views

app_name = "homepage"

urlpatterns = [
	url(r'^(?P<username>[a-zA-Z]+)/$', views.index, name = 'index'),
        url(r'logoutuser/$',views.logoutuser, name = 'logoutuser')
]

