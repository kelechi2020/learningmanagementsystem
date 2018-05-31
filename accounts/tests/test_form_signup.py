# coding=utf-8
from django.test import TestCase

from accounts.forms import StudentSignUpForm,InstructorSignUpForm,ObserverSignUpForm


class StudentSignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = StudentSignUpForm()
        expected = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

class InstructorSignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = InstructorSignUpForm()
        expected = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

class ObserverSignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = ObserverSignUpForm()
        expected = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', ]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)