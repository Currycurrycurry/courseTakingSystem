# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
# from .managers import AccountManager

class Account(models.Model):
    id = models.TextField(db_column='ID',primary_key=True)  # Field name made lowercase.
    password = models.TextField()
    role = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'account'

class Classroom(models.Model):
    classroom_no = models.TextField(primary_key=True)
    capacity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'classroom'


class Course(models.Model):
    course_id = models.TextField(primary_key=True)
    title = models.TextField()
    credits = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'course'


class Exam(models.Model):
    course_id = models.TextField(primary_key=True)
    section_id = models.TextField(primary_key=True)
    classroom_no = models.ForeignKey(Classroom, models.DO_NOTHING, db_column='classroom_no', blank=True, null=True)
    day = models.IntegerField()
    type = models.IntegerField()
    start_time = models.TextField(blank=True, null=True)
    end_time = models.TextField()
    open_note_flag = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exam'
        unique_together = ("course_id","section_id")


class ExamOld(models.Model):
    section = models.ForeignKey('SectionOld', models.DO_NOTHING,primary_key=True)
    classroom_no = models.ForeignKey(Classroom, models.DO_NOTHING, db_column='classroom_no', blank=True, null=True)
    day = models.IntegerField()
    type = models.IntegerField()
    start_time = models.TextField(blank=True, null=True)
    end_time = models.TextField()
    open_note_flag = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exam_old'


class Instructor(models.Model):
    instructor_id = models.TextField(blank=True,primary_key=True)
    instructor_name = models.TextField(blank=True, null=True)
    instructor_class = models.TextField(blank=True, null=True)
    dept_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instructor'


class Section(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING,primary_key=True)
    section_id = models.IntegerField(primary_key=True)
    time = models.TextField()
    classroom_no = models.TextField(blank=True, null=True)
    lesson = models.IntegerField()
    limit = models.IntegerField()
    day = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'section'
        unique_together = ("course","section_id")


class SectionOld(models.Model):
    section_id = models.TextField(primary_key=True)
    title = models.TextField()
    time = models.TextField()
    classroom_no = models.TextField(blank=True, null=True)
    lesson = models.IntegerField()
    dept_name = models.TextField()
    limit = models.IntegerField()
    credits = models.IntegerField()
    day = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'section_old'


class Student(models.Model):
    student_id = models.TextField(primary_key=True)
    student_name = models.TextField()
    student_major = models.TextField()
    student_dept_name = models.TextField()
    student_total_credit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'student'


class Takes(models.Model):
    course_id = models.TextField(primary_key=True)
    section_id = models.IntegerField(primary_key=True)
    student = models.ForeignKey(Student, models.DO_NOTHING,primary_key=True)
    grade = models.TextField(blank=True, null=True)
    drop_flag = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'takes'
        unique_together = ("course_id","section_id","student")


class TakesOld(models.Model):
    drop_flag = models.IntegerField()
    grade = models.CharField(max_length=10)
    section = models.ForeignKey(SectionOld, models.DO_NOTHING,primary_key=True)
    student = models.ForeignKey(Student, models.DO_NOTHING,primary_key=True)

    class Meta:
        managed = False
        db_table = 'takes_old'


class Teaches(models.Model):
    instuctor = models.ForeignKey(Instructor, models.DO_NOTHING,primary_key=True)
    course_id = models.TextField(primary_key=True)
    section_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'teaches'
        unique_together = ("instuctor","course_id","section_id")


class TeachesOld(models.Model):
    section = models.ForeignKey(SectionOld, models.DO_NOTHING,primary_key=True)
    instructor = models.ForeignKey(Instructor, models.DO_NOTHING,primary_key=True)

    class Meta:
        managed = False
        db_table = 'teaches_old'
        




# class
