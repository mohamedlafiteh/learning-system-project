from django.db import models

# Create your models here.

from quizes.models import Quiz

class Question(models.Model):
    question_title = models.CharField(max_length=180)
    user_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.question_title)

    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    answer_title = models.CharField(max_length=180)
    is_correct = models.BooleanField(default=False)
    quiz_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.quiz_question.question_title}, answer: {self.answer_title}, correct: {self.is_correct}"