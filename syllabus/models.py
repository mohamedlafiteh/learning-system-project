from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
import os
# Create your models here.

class Level(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=500,blank=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Subname(models.Model):
    subname_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='subnames')
    description = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.subname_id)
        super().save(*args, **kwargs)

def files_save(instance, filename):
    upload_to = 'Images/'
    check = filename.split('.')[-1]
    if instance.lecture_id:
        filename = 'lecture_files/{}/{}.{}'.format(instance.lecture_id,instance.lecture_id, check)
        if os.path.exists(filename):
            new_name = str(instance.lecture_id) + str('1')
            filename =  'lecture_images/{}/{}.{}'.format(instance.lecture_id,new_name, check)
    return os.path.join(upload_to, filename)

class Lecture(models.Model):
    lecture_id = models.CharField(max_length=100, unique=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    user_created_lecture = models.ForeignKey(User,on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    subname = models.ForeignKey(Subname, on_delete=models.CASCADE,related_name='lectures')
    name = models.CharField(max_length=250)
    chapter = models.PositiveSmallIntegerField(verbose_name="Chapter")
    slug = models.SlugField(null=True, blank=True)
    lecture_video = models.FileField(upload_to=files_save,verbose_name="Video", blank=True, null=True)
    lecture_presentations = models.FileField(upload_to=files_save,verbose_name="Presentations", blank=True)
    lecture_notes = models.FileField(upload_to=files_save,verbose_name="Notes", blank=True)
    
    class Meta:
        ordering = ['chapter']

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug=slugify(self.name)
        super().save(*args,**kwargs)  

    def get_absolute_url(self):
        return reverse('syllabus:lecture_list', kwargs={'slug':self.subname.slug, 'level':self.level.slug})

class Question(models.Model):
    lecture_name = models.ForeignKey(Lecture,null=True, on_delete=models.CASCADE,related_name='questions')
    question_name = models.CharField(max_length=100, blank=True)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    question_body = models.TextField(max_length=500)
    question_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.question_name = slugify("Question created by" + ":-" + str(self.sender) + str(self.question_date))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question_name

    class Meta:
        ordering = ['-question_date']

class Answer(models.Model):
    q_name = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='answers')
    answer_body = models.TextField(max_length=500)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    answer_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Answer to " + str(self.q_name.question_name)


# class Assessment(models.Model):
#     learner = models.ForeignKey(User,on_delete=models.CASCADE)
#     mark=models.PositiveIntegerField()
#     question=models.CharField(max_length=600)
#     option1=models.CharField(max_length=200)
#     option2=models.CharField(max_length=200)
#     option3=models.CharField(max_length=200)
#     cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'))
#     answer=models.CharField(max_length=200,choices=cat)
#     date = models.DateTimeField(auto_now_add=True)
#
# class Result(models.Model):
#     learner = models.ForeignKey(User,on_delete=models.CASCADE)
#     assessment = models.ForeignKey(Assessment,on_delete=models.CASCADE)
#     mark = models.PositiveIntegerField()
#     date = models.DateTimeField(auto_now_add=True)
