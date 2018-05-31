
from django.test import TestCase
from django.urls import resolve, reverse

from accounts.models import User
from course.models import Course
from discussion.models import Board, Topic, Post
from discussion.views import topic_posts


class TopicPostsTests(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = '123'

        user = User.objects.create_user(username='john', email='john@doe.com', password='123', is_instructor=True)
        self.course = Course.objects.create(creator=user, title="all we do is win win win", description="olowogbo")
        board = Board.objects.create(name='Django', description='Django board.', course=self.course,
                                          created_by=user)
        topic = Topic.objects.create(subject='Hello, world', board=board, starter=user)
        Post.objects.create(message='Lorem ipsum dolor sit amet', topic=topic, created_by=user)
        url = reverse('topic_posts', kwargs={'pk': board.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/discussion/boards/1/topics/1/')
        self.assertEquals(view.func, topic_posts)