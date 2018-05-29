from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from accounts.decorators import admin_required
from accounts.models import User


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_instructor:
            return redirect('instructor:quiz_change_list')
        elif request.user.is_staff:
            return redirect('admin_home')
        elif request.user.is_teaching_assistant:
            return redirect('student:quiz_list')
        elif request.user.is_student:
            return redirect('student:quiz_list')
        elif request.user.is_observer:
            return redirect('student:quiz_list')
    return redirect('login')


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


@method_decorator([login_required, admin_required], name='dispatch')
class InstructorsListView(AjaxableResponseMixin, ListView):
    """
    Returns list of quiz created by the currently logged in tutor
    """
    model = User
    ordering = ('username', )
    context_object_name = 'accounts'
    template_name = 'account_list.html'

    def get_queryset(self):
        """
        Overrides th default queryset method to return quizzes by the currently logged in user
        :return:
        """
        queryset = User.objects.filter(is_instructor=True)
        return queryset


@method_decorator([login_required, admin_required], name='dispatch')
class StudentsListView(AjaxableResponseMixin, ListView):
    """
    Returns list of quiz created by the currently logged in tutor
    """
    model = User
    ordering = ('username', )
    context_object_name = 'accounts'
    template_name = 'account_list.html'

    def get_queryset(self):
        """
        Overrides th default queryset method to return quizzes by the currently logged in user
        :return:
        """
        queryset = User.objects.filter(is_student=True)
        return queryset


@method_decorator([login_required, admin_required], name='dispatch')
class ObserversListView(AjaxableResponseMixin, ListView):
    """
    Returns list of quiz created by the currently logged in tutor
    """
    model = User
    ordering = ('username', )
    context_object_name = 'accounts'
    template_name = 'account_list.html'

    def get_queryset(self):
        """
        Overrides th default queryset method to return quizzes by the currently logged in user
        :return:
        """
        queryset = User.objects.filter(is_observer=True)
        return queryset


def account_delete(request, pk):
    account = get_object_or_404(User, pk=pk)
    data = dict()
    if request.method == 'POST':
        if account.is_student:
            account.delete()
            accounts = User.objects.filter(is_student=True)
        elif account.is_instructor:
            account.delete()
            accounts = User.objects.filter(is_instructor=True)
        elif account.is_observer:
            account.delete()
            accounts = User.objects.filter(is_observer=True)
        data['form_is_valid'] = True  # This is just to play along with the existing code

        data['html_book_list'] = render_to_string('account/includes/partial_account_list.html', {
            'accounts': accounts
        })
    else:
        context = {'accounts': account}
        data['html_form'] = render_to_string('account/includes/partial_account_delete.html', context, request=request, )
    return JsonResponse(data)