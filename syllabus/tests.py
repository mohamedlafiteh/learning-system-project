from django.test import TestCase

# Create your tests here.
from .models import Level


class SyllabusTest(TestCase):
    def setUp(self):
        self.level = Level()
        self.level.name = "national 4 maths"
        self.level.description = "learning maths"
        self.level.save()

    def test_fields(self):
        # record=Level.objects.filter(slug= self.level.slug)[0]
        record=Level.objects.get(pk=self.level.pk)
        self.assertEqual(record,self.level)

    def test_slug_save(self):
        self.assertEqual(self.level.slug,'national-4-maths')

    # def test_get_absolute_url(self):
    #     level = Level()
    #     level.name = "national 4 maths"
    #     level.save()
    #     self.assertEqual(level.get_absolute_url(),"/%s-%s/" %(level.id,level.slug) )


