from django.test import TestCase
from syllabus.models import  Lecture

# Create your tests here.
from django.contrib.auth.models import User
import datetime

from .models import Question,Answer
from quizes.models import Quiz


class QuestionsTest(TestCase):
    def setUp(self):


        # lecture setup
        self.user1 = User.objects.create_user(username='mo', password='12345')
        self.lecture = Lecture()
        self.lecture.name = "addition"
        self.lecture.chapter = 1
        self.lecture.user_created_lecture = User.objects.get(pk=self.user1.pk)
        self.lecture.save()

        #quiz setup
        self.quiz = Quiz()
        self.quiz.lecture_na=Lecture.objects.get(pk=self.lecture.pk)
        self.quiz.quiz_name = "addition"
        self.quiz.quiz_title = "maths"
        self.quiz.questions_number=5
        self.quiz.pass_score=50
        self.quiz.quiz_time=60
        self.quiz.save()

        # question setup
        self.question = Question()
        self.question.question_title="what is the result of 1+1"
        self.quiz=Quiz.objects.get(pk=self.quiz.pk)
        self.time_created=datetime.datetime.now()


    def test_model_str(self):
        self.assertEqual(self.question.question_title, "what is the result of 1+1")


