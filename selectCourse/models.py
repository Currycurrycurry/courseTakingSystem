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
    password = models.TextField()
    role = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'acount'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    last_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Classroom(models.Model):
    classroom_no = models.TextField()
    capacity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'classroom'


class Course(models.Model):
    course_id = models.TextField()
    title = models.TextField()
    credits = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'course'


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Exam(models.Model):
    course_id = models.TextField()
    section_id = models.TextField()
    classroom_no = models.ForeignKey(Classroom, models.DO_NOTHING, db_column='classroom_no', blank=True, null=True)
    day = models.IntegerField()
    type = models.IntegerField()
    start_time = models.TextField(blank=True, null=True)
    end_time = models.TextField()
    open_note_flag = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exam'


class ExamOld(models.Model):
    section = models.ForeignKey('SectionOld', models.DO_NOTHING)
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
    time = models.TextField()
    classroom_no = models.TextField(blank=True, null=True)
    lesson = models.IntegerField()
    limit = models.IntegerField()
    day = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'section'


class SectionOld(models.Model):
    section_id = models.TextField()
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
    student_id = models.TextField()
    student_name = models.TextField()
    student_major = models.TextField()
    student_dept_name = models.TextField()
    student_total_credit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'student'


class Takes(models.Model):
    course_id = models.TextField()
    section_id = models.IntegerField()
    student = models.ForeignKey(Student, models.DO_NOTHING)
    grade = models.TextField(blank=True, null=True)
    drop_flag = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'takes'


class TakesOld(models.Model):
    drop_flag = models.IntegerField()
    grade = models.CharField(max_length=10)
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


class Time(models.Model):
    day = models.CharField(max_length=20)
    end_time = models.IntegerField()
    end_week = models.IntegerField()
    start_week = models.IntegerField()
    start_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'time'