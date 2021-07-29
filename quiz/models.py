import random

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)
#quiz
class Quiz(models.Model):
    learner_na= models.ForeignKey(User,null=True, on_delete=models.CASCADE,related_name='qs')
    quiz_name = models.CharField(max_length=100,null=True)
    quiz_title = models.CharField(max_length=100,null=True)
    questions_number = models.IntegerField()
    quiz_time = models.IntegerField(help_text="Time in minutes",null=True)
    pass_score = models.IntegerField(help_text="Score in %",null=True)
    difficulty_status = models.CharField(max_length=6, choices=CHOICES)

    def __str__(self):
        return f"{self.quiz_name}-{self.quiz_title}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.questions_number]

    class Meta:
        verbose_name_plural = 'Quizes'

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='%(class)s_requests_created')
    score = models.FloatField()


    def __str__(self):
        return str(self.pk)


