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
from django.conf.urls import url, include
from django.contrib import admin

from accounts.view import SignUpView, home
from accounts.views.assistant_signup import AssistantSignUpView
from accounts.views.guest_signup import GuestSignUpView
from accounts.views.instructor_signup import InstructorSignUpView
from accounts.views.student_signup import StudentSignUpView

urlpatterns = [
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^instructor/', include('instructor.urls')),
    url(r'^student/', include('student.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/signup/$', SignUpView.as_view(), name='signup'),
    url(r'^accounts/signup/student/$', StudentSignUpView.as_view(), name='student_signup'),
    url(r'^accounts/signup/instructor/$', InstructorSignUpView.as_view(), name='instructor_signup'),
    url(r'^accounts/signup/assistant/$', AssistantSignUpView.as_view(), name='assistant_signup'),
    url(r'^accounts/signup/guest/$', GuestSignUpView.as_view(), name='guest_signup'),

]
