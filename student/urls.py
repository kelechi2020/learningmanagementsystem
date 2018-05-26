# coding=utf-8
from django.urls import include, path
from accounts.views import classroom
from course.views import CourseDetailView
from student.views import QuizListView, TakenQuizListView, take_quiz, CourseListView, course_registration, \
    RegisteredCourseListView

urlpatterns = [
    path('', classroom.home, name='home'),

    path('student/', include(([
        path('', CourseListView.as_view(), name='course_change_list'),
        path('viewcourse/<int:course_pk>/', CourseDetailView.as_view(), name='course_detail'),
        path('registered/course', RegisteredCourseListView.as_view(), name='registered_course_list'),
        path('register/<int:course_pk>/', course_registration, name='register_course'),
        path('quiz', QuizListView.as_view(), name='quiz_list'),
        path('taken/', TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', take_quiz, name='take_quiz'),
    ], 'student'), namespace='student')),
]
