from django.urls import include, path

from accounts.views import classroom
from instructor.views import QuizListView, QuizCreateView, QuizUpdateView, QuizDeleteView, QuizResultsView, \
    question_add, question_change, QuestionDeleteView

urlpatterns = [
    # path('', classroom.home, name='home'),

    path('instructor/', include(([
        path('', QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', QuestionDeleteView.as_view(), name='question_delete'),
    ], 'instructor'), namespace='teachers')),
]
