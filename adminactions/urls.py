from django.urls import path

from accounts.view import account_delete, InstructorsListView, StudentsListView, ObserversListView
from adminactions.views import admin_landing_page

urlpatterns = [
    path('adminhome/', admin_landing_page, name='admin_home'),
    path('view-instructor-accounts/', InstructorsListView.as_view(), name='instructor_accounts'),
    path('view-student-accounts/', StudentsListView.as_view(), name='student_accounts'),
    path('view-observer-accounts/', ObserversListView.as_view(), name='observer_accounts'),
    path('delete-accounts/<int:pk>/', account_delete, name='book_delete')
]