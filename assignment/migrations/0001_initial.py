# Generated by Django 2.0.5 on 2018-05-28 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        ('instructor', '0001_initial'),
        ('student', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_title', models.CharField(max_length=100, verbose_name='Assignment Title ')),
                ('assign_description', models.CharField(max_length=100, verbose_name='Assignment Description')),
                ('assignment_body', models.TextField(verbose_name='Assignment Content')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('assignment_due_date', models.DateTimeField()),
                ('course_title', models.CharField(max_length=200, verbose_name='Course Title')),
                ('topic_title', models.CharField(max_length=200, verbose_name='Topic Title')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='course.Course', verbose_name='Course name')),
                ('created_by', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='instructor.Instructor')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='course.Topic', verbose_name='Course Topic')),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='File Name')),
                ('file_description', models.CharField(max_length=200, verbose_name='Course Title')),
                ('file', models.FileField(upload_to='files/')),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_date', models.DateTimeField()),
                ('review', models.CharField(max_length=200)),
                ('rating', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubmittedAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('assignment_body', models.TextField()),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assignment.Assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='student.StudentProfile')),
            ],
        ),
        migrations.CreateModel(
            name='SubmittedAssignmentFiles',
            fields=[
                ('assignmentattachment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='assignment.AssignmentAttachment')),
            ],
            bases=('assignment.assignmentattachment',),
        ),
        migrations.AddField(
            model_name='assignmentreview',
            name='submitted_assignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assignment.SubmittedAssignment'),
        ),
        migrations.AddField(
            model_name='assignmentattachment',
            name='uploaded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='submittedassignment',
            name='attached_files',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assignment.SubmittedAssignmentFiles'),
        ),
    ]
