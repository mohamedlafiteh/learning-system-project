from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class app_user(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    
    instructor = 'instructor'
    learner = 'learner'
    app_users = [(instructor ,'instructor'),(learner , 'learner'),]

    app_user = models.CharField(max_length=10, choices=app_users, default=learner)


def __str__(self):
        return self.user.username


