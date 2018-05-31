from django.test import TestCase
from django.urls import reverse, resolve

from accounts.models import User
from accounts.views.guest_signup import ObserverSignUpView
from accounts.views.instructor_signup import InstructorSignUpView
from accounts.views.student_signup import StudentSignUpView


class SignUpTests(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password, is_staff=True)
        self.client.login(username=self.username, password=self.password)
        self.student_signup_url = reverse('student_signup')
        self.instructor_signup_url = reverse('instructor_signup')
        self.observer_signup_url = reverse('guest_signup')


    def test_student_signup_status_code(self):
        url = self.student_signup_url
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_instructor_signup_status_code(self):
        url = self.observer_signup_url
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_observer_signup_status_code(self):
        url = self.observer_signup_url
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_student_signup_url_resolves_signup_view(self):
        view = resolve('/adminact/accounts/signup/student/')
        self.assertEquals(view.func.view_class, StudentSignUpView)

    def test_instructor_signup_url_resolves_signup_view(self):
        view = resolve('/adminact/accounts/signup/instructor/')
        self.assertEquals(view.func.view_class, InstructorSignUpView)

    def test_observer_signup_url_resolves_signup_view(self):
        view = resolve('/adminact/accounts/signup/guest/')
        self.assertEquals(view.func.view_class, ObserverSignUpView)


class InvalidInstrucorSignUpTests(TestCase):
    def setUp(self):
        url = reverse('instructor_signup')
        self.response = self.client.post(url, {})

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())