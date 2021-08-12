from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
import datetime

from .models import Lecture, LectureGoals


class SyllabusTest(TestCase):
    def setUp(self):
        #level setup
        # lecture setup
        self.user1=User.objects.create_user(username='mohamed',password='12345')
        self.lecture = Lecture()
        self.lecture.name = "addition"
        self.lecture.chapter = 1
        self.lecture.user_created_lecture=User.objects.get(pk=self.user1.pk)
        self.time_created=datetime.datetime.now()
        self.lecture.save()


    # lecture model testing
    def test_lecture_fields(self):
        record = Lecture.objects.get(pk=self.lecture.pk)
        self.assertEqual(record, self.lecture)

    def test_lecture_model_str(self):
        self.assertEqual(self.lecture.name, "addition")

