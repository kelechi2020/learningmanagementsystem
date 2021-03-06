
from django.test import TestCase
from django.urls import resolve, reverse

from accounts.models import User
from accounts.view import home
from course.models import Course
from discussion.forms import NewTopicForm
from discussion.models import Board, Topic, Post
from discussion.views import board_topics, new_topic


class HomeTests(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password,
                                             is_instructor=True)
        self.course = Course.objects.create(creator=self.user, title="all we do is win win win", description="olowogbo")
        self.board = Board.objects.create(name='Django', description='Django board.', course=self.course,
                                          created_by=self.user)

        url = reverse('home')
        self.response = self.client.get(url)

    #test to check if a usrl returns the proper view
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


class BoardTopicTest(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password,
                                             is_instructor=True)
        self.course = Course.objects.create(creator=self.user, title="all we do is win win win", description="olowogbo")
        Board.objects.create(name='Django', description='Django board.', course=self.course,
                             created_by=self.user)

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topic_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/discussion/boards/1/')
        self.assertEquals(view.func, board_topics)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        home_page_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(home_page_url))


class NewTopicTests(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = '123'
        user  = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password,
                                 is_instructor=True)
        self.course = Course.objects.create(creator=user, title="all we do is win win win", description="olowogbo")

        Board.objects.create(name='Django', description='Django board.', course=self.course,
                             created_by=user)

        self.client.login(username='john', password='123')


    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_resolves_new_topic_view(self):
        view = resolve('/discussion/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))

    def test_csrf(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data ={
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())


    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    

