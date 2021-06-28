from django.contrib import admin

# Register your models here.
from quiz.models import Assessment,Results

# Register your models here.

admin.site.register(Assessment)
admin.site.register(Results)