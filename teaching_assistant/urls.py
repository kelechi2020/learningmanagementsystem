from django.urls import include, path

from .views import classroom, students, instructor

urlpatterns = [
    path('', classroom.home, name='home'),


    path('instructor/', include(([
        path('', instructor.QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', instructor.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', instructor.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', instructor.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', instructor.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', instructor.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', instructor.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', instructor.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='instructor')),
]
