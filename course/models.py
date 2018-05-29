from django.db import models

# Create your models here.
from django.shortcuts import get_object_or_404

from accounts.models import User
from instructor.models import Instructor


class Course(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT,related_name='courses')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,blank=True)
    image = models.FileField(upload_to='course', blank=True)
    blob = models.CharField(max_length=500, blank=True)
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

