from django.contrib import admin

# Register your models here.
from .models import Acount,Student,Classroom,Instructor,Course,Section,SectionOld,Takes,TakesOld,Teaches,TeachesOld,Exam,ExamOld

admin.site.register(Acount)
admin.site.register(Student)
admin.site.register(Classroom)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(SectionOld)
admin.site.register(Takes)
admin.site.register(TakesOld)
admin.site.register(Teaches)
admin.site.register(TeachesOld)
# admin.site.register(Time)
admin.site.register(ExamOld)
admin.site.register(Exam)









