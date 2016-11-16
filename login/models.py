from django.db import models
from django.contrib.auth.models import User

class NewUser(User):
    isOnline = models.BooleanField(default = False)
    friends = models.ManyToManyField("self")

    def __str__(self):
        return self.username+";"+self.password

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    num_of_lessons = models.IntegerField(default=0)
    image= models.CharField(max_length=200, default=None)
    #Quickreference sheet
    #gif library
    def __str__(self):
        return self.course_name+";"+str(self.num_of_lessons)

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson_name = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    summary = models.CharField(max_length=20000, default=None)
    expected_output = models.CharField(max_length=200, default=None)
    #point_value
    #video
    def __str__(self):
        return self.course.course_name+";"+self.lesson_name

class Progress(models.Model):
    newuser = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)
    progress_until_now = models.CharField(max_length=20000)
    def __str__(self):
        return self.newuser.username+";"+self.progress_until_now

class Challenge(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    challenge_name = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    expected_output = models.CharField(max_length=200, default=None)
    def __str__(self):
        return self.lesson.lesson_name+";"+self.challenge_name




    
