# coding=utf-8
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import CreateView

from accounts.forms import ObserverSignUpForm
from accounts.models import User


class ObserverSignUpView(CreateView):
    model = User
    form_class = ObserverSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Observer'
        messages.success(self.request, "Observer Account Created Successfuly")
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()

        return redirect('home')