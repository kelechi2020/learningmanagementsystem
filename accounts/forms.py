from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from accounts.models import User, ObserverProfile
from instructor.models import Instructor
from student.models import StudentProfile
from teaching_assistant.models import TeachingAssistant


class InstructorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_instructor = True
        if commit:
            user.save()
            Instructor.objects.create(user=user)
        return user

class AssistantSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_course_assistant = True
        if commit:
            user.save()
            TeachingAssistant.objects.create(user=user)
        return user


class StudentSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        StudentProfile.objects.create(user=user)
        return user


class ObserverSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_observer = True
        if commit:
            user.save()
            ObserverProfile.objects.create(user=user)
        return user
