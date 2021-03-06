from django.urls import include, path
from course.views import CourseListView, CourseUpdateView, CourseDeleteView, TopicListView, \
    TopicCreateView, TopicUpdateView, TopicDeleteView
from instructor.views import QuizListView, QuizCreateView, QuizUpdateView, QuizDeleteView, QuizResultsView, \
    question_add, question_change, QuestionDeleteView, CourseDetailView

urlpatterns = [
    # path('', classroom.home, name='home'),
    path('instructor/', include(([
        path('', CourseListView.as_view(), name='course_change_list'),
        path('course/<int:pk>/', CourseUpdateView.as_view(), name='course_change'),
        path('course/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
        path('coursedetail/<int:course_pk>/', CourseDetailView.as_view(), name='course_detail'),

        path('topic', TopicListView.as_view(), name='topic_change_list'),
        path('topic/add/<int:course_pk>/', TopicCreateView.as_view(), name='topic_add'),
        path('topic/<int:pk>/', TopicUpdateView.as_view(), name='topic_change'),
        path('topic/<int:pk>/delete/', TopicDeleteView.as_view(), name='topic_delete'),

        path('quiz', QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/<int:course_pk>/', QuizCreateView.as_view(), name='quiz_add'),
        # path('quiz/add/<int:course_pk>/', quizcreate, name='quiz_add'),
        path('quiz/<int:pk>/', QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', QuestionDeleteView.as_view(), name='question_delete'),
    ], 'instructor'), namespace='instructor')),
]