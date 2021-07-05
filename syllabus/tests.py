from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
import datetime

from .models import Level, Subname, Lecture, LectureGoals


class SyllabusTest(TestCase):
    def setUp(self):
        #level setup
        self.level = Level()
        self.level.name = "national 4 maths"
        self.level.description = "learning maths"
        self.level.save()

        #subname setup
        self.subname = Subname()
        self.subname.name = "easy maths"
        self.subname.description = "learning best way maths"
        self.subname.level=Level.objects.get(pk=self.level.pk)
        self.subname.save()

        # lecture setup
        self.user1=User.objects.create_user(username='mo',password='12345')
        self.lecture = Lecture()
        self.lecture.name = "addition"
        self.lecture.description = "learning best way maths"
        self.lecture.chapter = 1
        self.lecture.user_created_lecture=User.objects.get(pk=self.user1.pk)
        self.lecture.level = Level.objects.get(pk=self.level.pk)
        self.lecture.subname = Subname.objects.get(pk=self.subname.pk)
        self.lecture.save()



    #level model testing
    def test_level_fields(self):
        record=Level.objects.get(pk=self.level.pk)
        self.assertEqual(record,self.level)

    def test_model_str(self):
        self.assertEqual(self.level.name, "national 4 maths")

    def test_slug_save(self):
        self.assertEqual(self.level.slug,'national-4-maths')

    def test_testlevelpage_url(self):
        response= self.client.get('/')
        self.assertEqual(response.status_code,200)

    # subname model testing
    def test_test_subname_fields(self):
        record = Subname.objects.get(pk=self.subname.pk)
        self.assertEqual(record, self.subname)

    def test_subname_model_str(self):
        self.assertEqual(self.subname.name, "easy maths")

    # lecture model testing
    def test_lecture_fields(self):
        record = Lecture.objects.get(pk=self.lecture.pk)
        self.assertEqual(record, self.lecture)

    def test_lecture_model_str(self):
        self.assertEqual(self.lecture.name, "addition")

