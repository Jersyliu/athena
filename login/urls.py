from django.conf.urls import url

from . import views

app_name = "login"

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
    url(r'dologin/$', views.dologin, name = "dologin"),
    url(r'doregister/$', views.doregister, name = "doregister"),
    url(r'register/$', views.register, name = "register"),
  
]
