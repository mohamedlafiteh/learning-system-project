import random

from django.db import models
from syllabus.models import Lecture
from django.contrib.auth.models import User
# Create your models here.
DIFF_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)
#quiz
class Quiz(models.Model):
    learner_na= models.ForeignKey(User,null=True, on_delete=models.CASCADE,related_name='qs')
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="duration of the quiz in minutes")
    required_score_to_pass = models.IntegerField(help_text="required score in %")
    difficulty = models.CharField(max_length=6, choices=DIFF_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

    class Meta:
        verbose_name_plural = 'Quizes'


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='%(class)s_requests_created')
    score = models.FloatField()

    def __str__(self):
        return str(self.pk)







# Create your models here.
# class Assessment(models.Model):
#
#     mark=models.PositiveIntegerField()
#     question=models.CharField(max_length=600)
#     option1=models.CharField(max_length=200)
#     option2=models.CharField(max_length=200)
#     option3=models.CharField(max_length=200)
#     cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'))
#     answer=models.CharField(max_length=200,choices=cat)
#     date = models.DateTimeField(auto_now_add=True)
#
# class Results(models.Model):
#     learner = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
#     mark = models.PositiveIntegerField()
#     date = models.DateTimeField(auto_now_add=True)