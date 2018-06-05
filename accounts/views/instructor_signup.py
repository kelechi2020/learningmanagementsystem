from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from accounts.forms import InstructorSignUpForm
from accounts.models import User


class InstructorSignUpView(CreateView):
    model = User
    form_class = InstructorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Instructor'

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, "Instructor Account Created Successfuly")
        return redirect('home')