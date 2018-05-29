
from django.urls import path

from discussion.views import new_topic, board_topics, topic_posts, reply_topic, discussion_home,BoardCreateView

urlpatterns = [
    path('', discussion_home, name='discussion_home'),
    path('boards/new', BoardCreateView.as_view(), name='new_board'),
    path('boards/<int:pk>/new/', new_topic, name='new_topic'),
    path('boards/<int:pk>/', board_topics, name='board_topics'),
    path('boards/<int:pk>/topics/<int:topic_pk>/', topic_posts, name='topic_posts'),
    path('boards/<int:pk>/topics/<int:topic_pk>/reply/', reply_topic, name='reply_topic'),

]
