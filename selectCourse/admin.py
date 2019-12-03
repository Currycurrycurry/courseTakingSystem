from django.contrib import admin

# Register your models here.
from .models import Account,Student,Classroom,Instructor,Course,Section,SectionOld,Time_slot,Exam,ExamOld


admin.site.register(Student)
admin.site.register(Classroom)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(SectionOld)
admin.site.register(Time_slot)
admin.site.register(Exam)
admin.site.register(ExamOld)










