from django.db import models
from accounts.models import User


class Instructor(models.Model):
    """
    Instructors Profile
    """
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='instructor')
    photo = models.FileField(upload_to='tutor', null=True, blank=True)
    designation = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    course = models.ManyToManyField('course.Course')
    class Meta:
        verbose_name_plural = 'Instructor'

    def __str__(self):
        return self.user.username


