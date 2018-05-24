# Generated by Django 2.0.5 on 2018-05-23 12:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_remove_course_instructor'),
        ('discussion', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='board',
            options={'verbose_name_plural': 'Course Discussion'},
        ),
        migrations.AlterModelOptions(
            name='topic',
            options={'verbose_name_plural': 'Topic'},
        ),
        migrations.AddField(
            model_name='board',
            name='course',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.CASCADE, to='course.Course'),
            preserve_default=False,
        ),
    ]
