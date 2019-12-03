from django.contrib import admin

# Register your models here.
from .models import Student,Classroom,Instructor,Course,Section,CourseApplication,Instructor_Section,Student_Section,Time_slot

admin.site.register(Student)
admin.site.register(Classroom)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(CourseApplication)
admin.site.register(Instructor_Section)
admin.site.register(Student_Section)
admin.site.register(Time_slot)









