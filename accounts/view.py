from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from accounts.decorators import student_required


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_instructor:
            return redirect('instructor:course_change_list')
        else:
            return redirect('student:quiz_list')
    return redirect('login')
