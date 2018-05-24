from django.db import models

# Create your models here.
from accounts.models import User
from course.models import Course
from instructor.models import Instructor


class TeachingAssistant(models.Model):
    """
    Teaching Assistants Profile
    """

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='teaching_assistant')
    assist = models.ManyToManyField(Instructor)
    course = models.ManyToManyField(Course)
    photo = models.FileField(upload_to='tutor', null=True, blank=True)
    designation = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Assistant'

    def __str__(self):
        return self.user.username
