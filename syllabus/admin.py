from django.contrib import admin
from syllabus.models import Level,Subname,Lecture,Question,Answer,Assessment,Result

# Register your models here.

admin.site.register(Level)
admin.site.register(Subname)
admin.site.register(Lecture)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Assessment)
admin.site.register(Result)


