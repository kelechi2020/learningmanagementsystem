from django.urls import include, path

from accounts.views import classroom
from student.views import QuizListView, TakenQuizListView, take_quiz

urlpatterns = [
    path('', classroom.home, name='home'),

    path('students/', include(([
        path('', QuizListView.as_view(), name='quiz_list'),
        path('taken/', TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', take_quiz, name='take_quiz'),
    ], 'classroom'), namespace='students')),

]
