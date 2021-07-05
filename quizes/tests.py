from django.test import TestCase
from syllabus.models import Level, Subname, Lecture

# Create your tests here.
from django.contrib.auth.models import User
from datetime import datetime

from .models import Quiz


class QuizesTest(TestCase):
    def setUp(self):
        self.level = Level()
        self.level.name = "national 4 maths"
        self.level.description = "learning maths"
        self.level.save()

        # subname setup
        self.subname = Subname()
        self.subname.name = "easy maths"
        self.subname.description = "learning best way maths"
        self.subname.level = Level.objects.get(pk=self.level.pk)
        self.subname.save()

        # lecture setup
        self.user1 = User.objects.create_user(username='mo', password='12345')
        self.lecture = Lecture()
        self.lecture.name = "addition"
        self.lecture.description = "learning best way maths"
        self.lecture.chapter = 1
        self.lecture.user_created_lecture = User.objects.get(pk=self.user1.pk)
        self.lecture.level = Level.objects.get(pk=self.level.pk)
        self.lecture.subname = Subname.objects.get(pk=self.subname.pk)
        self.lecture.save()

        #quiz setup
        self.quiz = Quiz()
        self.quiz.lecture_na=Lecture.objects.get(pk=self.lecture.pk)
        self.quiz.name = "addition"
        self.quiz.topic = "maths"
        self.quiz.number_of_questions=5
        self.quiz.required_score_to_pass=50
        self.quiz.time=60
        self.quiz.save()


    #level model testing
    def test_quiz_fields(self):
        record=Quiz.objects.get(pk=self.quiz.pk)
        self.assertEqual(record,self.quiz)

    def test_model_str(self):
        self.assertEqual(self.quiz.name, "addition")
        self.assertEqual(self.quiz.topic, "maths")


    def test_url(self):
        print(self.quiz.pk)
        response= self.client.get('/')
        self.assertEqual(response.status_code,200)

