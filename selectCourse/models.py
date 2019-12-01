# -*- coding: UTF-8 -*-
from django.db import models
#类名：数据库表名
# class Test(models.Model):
#     name = models.CharField(max_length=20)



class Student(models.Model):
    student_id = models.BigIntegerField(primary_key=True,default=0)
    student_name = models.CharField(max_length=20)
    student_password = models.CharField(max_length=20)
    student_major = models.CharField(max_length=20)
    student_dept_name = models.CharField(max_length=20)
    student_total_credit = models.IntegerField(default=0)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'student'
        verbose_name = 'student'

class Instructor(models.Model):
    instructor_id = models.BigIntegerField(primary_key=True,default=0)
    instructor_name = models.CharField(max_length=20)
    instructor_password = models.CharField(max_length=20)
    salary = models.IntegerField(default=0)
    instructor_class = models.CharField(max_length=20,default="讲师")
    instructor_dept_name = models.CharField(max_length=20)
    root_flag = models.BooleanField(blank=False)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'instructor'
        verbose_name = 'instructor'

class Course(models.Model):
    course_id = models.IntegerField(primary_key=True,default=0)
    # course_code = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    credit = models.IntegerField(default=0) # unit:hour
    course_dept_name = models.CharField(max_length=20)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'course'
        verbose_name = 'course'

# class Department(models.Model):
#     dept_name = models.CharField(primary_key=True,max_length=20)

class Time_slot(models.Model):
    # time_slot_id = models.CharField(primary_key=True,max_length=20) #?
    day = models.CharField(max_length=20) #Monday
    start_week = models.IntegerField(default=0) # 1
    end_week = models.IntegerField(default=0)
    start_time = models.IntegerField(default=0) 
    end_time = models.IntegerField(default=0) 

    def __str__(self):
        return (self.day + start_week + "-" + end_week + " "+ start_time + "-" + end_time)

    class Meta:
        db_table = 'time'
        verbose_name = 'time'

class Classroom(models.Model):
    # building_name = models.CharField(primary_key=True,max_length=20)
    # room_no = models.IntegerField(default=0)
    classroom_no = models.CharField(primary_key=True,max_length=20) # char : hard to extract 
    capacity = models.IntegerField(default=200)

    def __str__(self):
        return self.classroom_no

    class Meta:
        db_table = 'classroom'
        verbose_name = 'classroom'

class Section(models.Model):
    section_id = models.CharField(primary_key=True,max_length=20)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    semester = models.CharField(default="第一学期",max_length=20)
    year = models.IntegerField(default="2017")
    limit = models.IntegerField(default=0) # max number of students
    time_slot_id = models.ForeignKey(Time_slot,on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)

    def __str__(self):
        return self.classroom_no

    class Meta:
        db_table = 'section'
        verbose_name = 'section'

class Student_Section(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    grade = models.CharField(max_length=1) #?

class Instructor_Section(models.Model):
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE)
    section = models.ForeignKey(Section,on_delete=models.CASCADE)

class Exam(models.Model):
    section = models.OneToOneField(Section,on_delete=models.CASCADE)
    type = models.BooleanField(blank=True)
    open_note_flag = models.BooleanField(blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)

class CourseApplication(models.Model):
    course =  models.ForeignKey(Course,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    application_time = models.DateField(auto_now=True)
    application_state = models.BooleanField(blank=False)


    






    







    







    

