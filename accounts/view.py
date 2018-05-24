from django.http import HttpResponse
from django.views.generic import TemplateView
from accounts.decorators import student_required


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


@student_required
def home(request):
    return HttpResponse("all i do is wi ")