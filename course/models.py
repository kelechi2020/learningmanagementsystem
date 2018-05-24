from django.db import models

# Create your models here.
from instructor.models import Instructor


class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.FileField(upload_to='course')
    blob = models.CharField(max_length=500)
    description = models.TextField()
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Course'

    def __str__(self):
        return self.title


class Topic(models.Model):
    topics_course = models.ForeignKey(Course, on_delete=models.PROTECT)
    topic_chapter = models.PositiveIntegerField()
    topic_title = models.CharField(max_length=200)
    topic_description = models.TextField()
    topic_duration = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = 'Topic'

    def __str__(self):
        return self.topic_title

