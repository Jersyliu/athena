from django.contrib import admin

from .models import NewUser, Course, Lesson, Progress, Challenge, ChallengeProgress, CourseLocation

# Register your models here.

admin.site.register(NewUser)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Progress)
admin.site.register(Challenge)
admin.site.register(ChallengeProgress)
admin.site.register(CourseLocation)
