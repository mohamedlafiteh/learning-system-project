from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
import os


# Create your models here.

#This model for the maths level on the first page
class Level(models.Model):
    name = models.CharField(max_length=70, unique=True)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=400, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

#This model for the maths subject on the second page
class Subname(models.Model):
    subname_id = models.CharField(max_length=70, unique=True)
    name = models.CharField(max_length=70)
    slug = models.SlugField(null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='subnames')
    description = models.TextField(max_length=400, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subname_id)
        super().save(*args, **kwargs)

#This function for uploading the lecture_video  and lecture_presentations
def files_save(l, n):
    save_dir = 'Images/'
    res = n.split('.')[-1]
    if l.lecture_id:
        n = 'all_files/{}/{}.{}'.format(l.lecture_id, l.lecture_id, res)
        if os.path.exists(n):
            name = str(l.lecture_id) + str('1')
            n = 'all_images/{}/{}.{}'.format(l.lecture_id, name, res)
    return os.path.join(save_dir, n)

#This model for the maths lecture on the third page
class Lecture(models.Model):
    lecture_id = models.CharField(max_length=70, unique=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    user_created_lecture = models.ForeignKey(User, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    subname = models.ForeignKey(Subname, on_delete=models.CASCADE, related_name='lectures')
    name = models.CharField(max_length=100)
    chapter = models.PositiveSmallIntegerField(verbose_name="Chapter")
    slug = models.SlugField(null=True, blank=True)
    lecture_video = models.FileField(upload_to=files_save, verbose_name="Video", blank=True, null=True)
    lecture_presentations = models.FileField(upload_to=files_save, verbose_name="Presentations", blank=True)

    class Meta:
        ordering = ['chapter']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('syllabus:lecture_list', kwargs={'slug': self.subname.slug, 'level': self.level.slug})

#This model for setting learning goal on the lecture
class LectureGoals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_lecture_goal")
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return str(self.user) + ' - ' + str(self.lecture)

#This model for the questions on the lecture
class Question(models.Model):
    lecture_name = models.ForeignKey(Lecture, null=True, on_delete=models.CASCADE, related_name='questions')
    question_name = models.CharField(max_length=200, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    question_body = models.TextField(max_length=600)
    question_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.question_name = slugify("Question created by" + ":-" + str(self.sender) + str(self.question_date))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question_name

    class Meta:
        ordering = ['-question_date']

#This model for the replys for the questions
class Answer(models.Model):
    q_name = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_body = models.TextField(max_length=600)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Answer to " + str(self.q_name.question_name)

#
