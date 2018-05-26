# coding=utf-8
from django.urls import include, path
from accounts.views import classroom
from student.views import QuizListView, TakenQuizListView, take_quiz, CourseListView, course_registration

urlpatterns = [
    path('', classroom.home, name='home'),

    path('student/', include(([
        path('', CourseListView.as_view(), name='course_change_list'),
        path('register/<int:course_pk>/', course_registration, name='register_course'),
        path('quiz', QuizListView.as_view(), name='quiz_list'),
        path('taken/', TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', take_quiz, name='take_quiz'),
    ], 'student'), namespace='student')),
]
