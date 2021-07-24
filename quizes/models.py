from django.db import models
import random
from syllabus.models import Lecture

CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
)
#quiz model
class Quiz(models.Model):
    lecture_na= models.ForeignKey(Lecture,null=True, on_delete=models.CASCADE,related_name='qs')
    quiz_name = models.CharField(max_length=120)
    quiz_title = models.CharField(max_length=120)
    questions_number = models.IntegerField()
    quiz_time = models.IntegerField(help_text="duration of the quiz in minutes")
    pass_score = models.IntegerField(help_text="required score in %")
    difficulty_status = models.CharField(max_length=6, choices=CHOICES)

    def __str__(self):
        return f"{self.quiz_name}-{self.quiz_title}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.questions_number]

    class Meta:
        verbose_name_plural = 'Quizes'