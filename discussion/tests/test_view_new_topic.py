from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from course.models import Course
from discussion.models import Board


class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password, is_instructor=True)
        self.course = Course.objects.create(creator=self.user,title="all we do is win win win", description="olowogbo")
        self.board = Board.objects.create(name='Django', description='Django board.', course=self.course, created_by=self.user)

        self.url = reverse('new_topic', kwargs={'pk': 1})
        self.response = self.client.get(self.url)
        self.client.login(username=self.username, password=self.password)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))