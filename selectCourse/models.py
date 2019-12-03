# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Acount(models.Model):
    id = models.TextField(db_column='ID')  # Field name made lowercase.
    password = models.TextField(blank=True, null=True)
    role = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acount'


class Classroom(models.Model):
    classroom_no = models.TextField()
    capacity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'classroom'


class Course(models.Model):
    course_id = models.TextField()
    title = models.TextField(blank=True, null=True)
    credits = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course'


class Exam(models.Model):
    course_id = models.TextField()
    section_id = models.TextField()
    classroom_no = models.ForeignKey(Classroom, models.DO_NOTHING, db_column='classroom_no', blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    start_time = models.TextField(blank=True, null=True)
    end_time = models.TextField(blank=True, null=True)
    open_note_flag = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exam'


class ExamOld(models.Model):
    section = models.ForeignKey('SectionOld', models.DO_NOTHING)
    classroom_no = models.ForeignKey(Classroom, models.DO_NOTHING, db_column='classroom_no', blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    start_time = models.TextField(blank=True, null=True)
    end_time = models.TextField(blank=True, null=True)
    open_note_flag = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exam_old'


class Instructor(models.Model):
    instructor_id = models.TextField(blank=True, null=True)
    instructor_name = models.TextField(blank=True, null=True)
    instructor_class = models.TextField(blank=True, null=True)
    dept_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instructor'


class Section(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING)
    section_id = models.IntegerField()
    time = models.TextField(blank=True, null=True)
    classroom_no = models.TextField(blank=True, null=True)
    lesson = models.IntegerField(blank=True, null=True)
    limit = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'section'


class SectionOld(models.Model):
    section_id = models.TextField()
    title = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    classroom_no = models.TextField(blank=True, null=True)
    lesson = models.IntegerField(blank=True, null=True)
    dept_name = models.TextField(blank=True, null=True)
    limit = models.IntegerField(blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'section_old'


class Student(models.Model):
    student_id = models.AutoField(primary_key = True)
    student_name = models.CharField(max_length=20)
    student_major = models.CharField(max_length=20)
    student_dept_name = models.CharField(max_length=20)
    student_total_credit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'student'


class Takes(models.Model):
    course_id = models.AutoField(primary_key = True)
    section_id = models.IntegerField()
    student = models.ForeignKey(Student, models.DO_NOTHING)
    grade = models.TextField(blank=True, null=True)
    drop_flag = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'takes'


class TakesOld(models.Model):
    drop_flag = models.IntegerField(blank=True, null=True)
    grade = models.CharField(max_length=1)
    section = models.ForeignKey(SectionOld, models.DO_NOTHING)
    student = models.ForeignKey(Student, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'takes_old'


class Teaches(models.Model):
    instuctor = models.ForeignKey(Instructor, models.DO_NOTHING)
    course_id = models.TextField()
    section_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'teaches'


class TeachesOld(models.Model):
    section = models.ForeignKey(SectionOld, models.DO_NOTHING)
    instructor = models.ForeignKey(Instructor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'teaches_old'

