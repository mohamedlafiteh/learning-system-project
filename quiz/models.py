from django.db import models
from syllabus.models import Lecture
from django.contrib.auth.models import User

# Create your models here.
# class Assessment(models.Model):
#     lecture = models.ForeignKey(Lecture,on_delete=models.CASCADE)
#     mark=models.PositiveIntegerField()
#     question=models.CharField(max_length=600)
#     option1=models.CharField(max_length=200)
#     option2=models.CharField(max_length=200)
#     option3=models.CharField(max_length=200)
#     cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'))
#     answer=models.CharField(max_length=200,choices=cat)
#     date = models.DateTimeField(auto_now_add=True)

# class Result(models.Model):
#     learner = models.ForeignKey(User,on_delete=models.CASCADE)
#     assessment = models.ForeignKey(Assessment,on_delete=models.CASCADE)
#     mark = models.PositiveIntegerField()
#     date = models.DateTimeField(auto_now_add=True)
