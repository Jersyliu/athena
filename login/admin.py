from django.contrib import admin

from .models import NewUser, Course, Lesson, Progress, Challenge

# Register your models here.

admin.site.register(NewUser)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Progress)
admin.site.register(Challenge)
