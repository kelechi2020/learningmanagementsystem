from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms

from accounts.models import User, ObserverProfile
from course.models import Course
from instructor.models import Instructor
from student.models import StudentProfile
from teaching_assistant.models import TeachingAssistant


class InstructorSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_instructor = True
        if commit:
            user.save()
            Instructor.objects.create(user=user)
        return user


class AssistantSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True )
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_course_assistant = True
        if commit:
            user.save()
            TeachingAssistant.objects.create(user=user)
        return user


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        StudentProfile.objects.create(user=user)
        return user


class ObserverSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,)
    last_name = forms.CharField(max_length=30, required=False, )
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_observer = True
        if commit:
            user.save()
            ObserverProfile.objects.create(user=user)
        return user


