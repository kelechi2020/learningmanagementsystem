# Generated by Django 2.0.5 on 2018-05-28 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        ('instructor', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeachingAssistant',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='teaching_assistant', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('photo', models.FileField(blank=True, null=True, upload_to='tutor')),
                ('designation', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('state', models.CharField(blank=True, max_length=200, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('assist', models.ManyToManyField(to='instructor.Instructor')),
                ('course', models.ManyToManyField(to='course.Course')),
            ],
            options={
                'verbose_name_plural': 'Assistant',
            },
        ),
    ]
