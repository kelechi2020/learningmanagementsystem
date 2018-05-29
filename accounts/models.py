from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extending the Abstract user class to add extra fields that allow a user assume
    one or more roles on the platform
    """
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_teaching_assistant = models.BooleanField(default=False)
    is_observer = models.BooleanField(default=False)


class ObserverProfile(models.Model):
    """
    Instructors Profile
    """
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='tutor')
    photo = models.FileField(upload_to='tutor', null=True, blank=True)
    designation = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Tutor'

    def __str__(self):
        return self.user.username


