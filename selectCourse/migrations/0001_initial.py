# Generated by Django 2.0 on 2019-12-04 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.TextField(db_column='ID', primary_key=True, serialize=False)),
                ('password', models.TextField()),
                ('role', models.IntegerField(primary_key=True)),
            ],
            options={
                'db_table': 'account',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('classroom_no', models.TextField(primary_key=True, serialize=False)),
                ('capacity', models.IntegerField()),
            ],
            options={
                'db_table': 'classroom',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.TextField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('credits', models.IntegerField()),
            ],
            options={
                'db_table': 'course',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('course_id', models.TextField(primary_key=True, serialize=False)),
                ('section_id', models.TextField(primary_key=True)),
                ('day', models.IntegerField()),
                ('type', models.IntegerField()),
                ('start_time', models.TextField(blank=True, null=True)),
                ('end_time', models.TextField()),
                ('open_note_flag', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'exam',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('instructor_id', models.TextField(blank=True, primary_key=True, serialize=False)),
                ('instructor_name', models.TextField(blank=True, null=True)),
                ('instructor_class', models.TextField(blank=True, null=True)),
                ('dept_name', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'instructor',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SectionOld',
            fields=[
                ('section_id', models.TextField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('time', models.TextField()),
                ('classroom_no', models.TextField(blank=True, null=True)),
                ('lesson', models.IntegerField()),
                ('dept_name', models.TextField()),
                ('limit', models.IntegerField()),
                ('credits', models.IntegerField()),
                ('day', models.IntegerField()),
            ],
            options={
                'db_table': 'section_old',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.TextField(primary_key=True, serialize=False)),
                ('student_name', models.TextField()),
                ('student_major', models.TextField()),
                ('student_dept_name', models.TextField()),
                ('student_total_credit', models.IntegerField()),
            ],
            options={
                'db_table': 'student',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExamOld',
            fields=[
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='selectCourse.SectionOld')),
                ('day', models.IntegerField()),
                ('type', models.IntegerField()),
                ('start_time', models.TextField(blank=True, null=True)),
                ('end_time', models.TextField()),
                ('open_note_flag', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'exam_old',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='selectCourse.Course')),
                ('section_id', models.IntegerField(primary_key=True)),
                ('time', models.TextField()),
                ('classroom_no', models.TextField(blank=True, null=True)),
                ('lesson', models.IntegerField()),
                ('limit', models.IntegerField()),
                ('day', models.IntegerField()),
            ],
            options={
                'db_table': 'section',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Takes',
            fields=[
                ('course_id', models.TextField(primary_key=True, serialize=False)),
                ('section_id', models.IntegerField(primary_key=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, to='selectCourse.Student')),
                ('grade', models.TextField(blank=True, null=True)),
                ('drop_flag', models.IntegerField()),
            ],
            options={
                'db_table': 'takes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TakesOld',
            fields=[
                ('drop_flag', models.IntegerField()),
                ('grade', models.CharField(max_length=10)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='selectCourse.SectionOld')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, to='selectCourse.Student')),
            ],
            options={
                'db_table': 'takes_old',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Teaches',
            fields=[
                ('instuctor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='selectCourse.Instructor')),
                ('course_id', models.TextField(primary_key=True)),
                ('section_id', models.IntegerField(primary_key=True)),
            ],
            options={
                'db_table': 'teaches',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TeachesOld',
            fields=[
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='selectCourse.SectionOld')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, to='selectCourse.Instructor')),
            ],
            options={
                'db_table': 'teaches_old',
                'managed': False,
            },
        ),
    ]
