from django.contrib import admin
from syllabus.models import Lecture,Question,Answer,LectureGoals

# Register your models here.


admin.site.register(Lecture)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(LectureGoals)



