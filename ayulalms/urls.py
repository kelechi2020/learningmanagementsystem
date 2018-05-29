# coding=utf-8
"""ayulalms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf.urls import include

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView,  \
     PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView,\
    PasswordChangeDoneView

from accounts.view import SignUpView, home
from accounts.views.assistant_signup import AssistantSignUpView
from accounts.views.guest_signup import ObserverSignUpView
from accounts.views.instructor_signup import InstructorSignUpView
from accounts.views.student_signup import StudentSignUpView

urlpatterns = (
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^$', home, name='home'),
    url(r'^adminact/', include('adminactions.urls')),
    url(r'^instructor/', include('instructor.urls')),
    url(r'^student/', include('student.urls')),
    url(r'^discussion/', include('discussion.urls')),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^login/$', LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^accounts/signup/$', SignUpView.as_view(), name='signup'),
    url(r'^accounts/signup/student/$', StudentSignUpView.as_view(), name='student_signup'),
    url(r'^accounts/signup/instructor/$', InstructorSignUpView.as_view(), name='instructor_signup'),
    url(r'^accounts/signup/assistant/$', AssistantSignUpView.as_view(), name='assistant_signup'),
    url(r'^accounts/signup/guest/$', ObserverSignUpView.as_view(), name='guest_signup'),
    url(r'^reset/$', PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'^reset/done/$',PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    url(r'^settings/password/$', PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$', PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),
)

