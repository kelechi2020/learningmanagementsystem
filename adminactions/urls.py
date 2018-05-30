from django.urls import path
from accounts.view import account_delete, InstructorsListView, StudentsListView, ObserversListView
from accounts.views.assistant_signup import AssistantSignUpView
from accounts.views.guest_signup import ObserverSignUpView
from accounts.views.instructor_signup import InstructorSignUpView
from accounts.views.student_signup import StudentSignUpView
from adminactions.views import admin_landing_page, assign_course_to_intructor, AdminCourseCreateView \
    , AdminCourseDetailView, AdminCourseListView

urlpatterns = [
    path('adminhome/', admin_landing_page, name='admin_home'),
    path('view-instructor-accounts/', InstructorsListView.as_view(), name='instructor_accounts'),
    path('view-student-accounts/', StudentsListView.as_view(), name='student_accounts'),
    path('view-observer-accounts/', ObserversListView.as_view(), name='observer_accounts'),
    path('delete-accounts/<int:pk>/', account_delete, name='account_delete'),


    path('list-courses/', AdminCourseListView.as_view(), name='admin_list_courses'),
    path('create-courses/', AdminCourseCreateView.as_view(), name='admin_create_courses'),
    path('view-course/<int:course_pk>/', AdminCourseDetailView.as_view(), name='admin_view_courses'),
    path('assign-courses/', assign_course_to_intructor, name='admin_assign_courses'),


    path('accounts/signup/student/', StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/instructor/', InstructorSignUpView.as_view(), name='instructor_signup'),
    path('accounts/signup/assistant/', AssistantSignUpView.as_view(), name='assistant_signup'),
    path('accounts/signup/guest/', ObserverSignUpView.as_view(), name='guest_signup'),

]