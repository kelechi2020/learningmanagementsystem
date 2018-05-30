from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView

from accounts.decorators import instructor_required, admin_required
from adminactions.forms import AdminCourseAssignmentForm

from course.models import Course


def admin_landing_page(request):
    return render(request, 'externals/admin_dashboard.html')


@method_decorator([login_required, admin_required], name='dispatch')
class AdminCourseCreateView(CreateView):
    model = Course
    fields = ('title', 'slug', 'image', 'description', 'blob')
    template_name = 'course_add_form.html'

    def form_valid(self, form):
        course = form.save(commit=False)
        course.creator = self.request.user
        messages.success(self.request, 'The Course was created with success! Go ahead and add some quiz now.')
        return redirect('admin_list_courses')

@login_required
@admin_required
def assign_course_to_intructor(request):
    submit_button = True
    if request.method == 'POST':
        form = AdminCourseAssignmentForm(data=request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            instructor = form.cleaned_data.get('instructor')
            course = form.cleaned_data.get('course')
            instructor.course.add(course)
            messages.success(request, "Course {0} was assgined to {1} successfuly".format(course.title, instructor.user.username))
    else:
        form = AdminCourseAssignmentForm()

    return render(request, 'take_quiz_form.html', {'form': form, 'submit_button': submit_button})


@method_decorator([login_required, admin_required], name='dispatch')
class AdminCourseListView(ListView):
    model = Course
    ordering = ('title', )
    context_object_name = 'courses'
    template_name = 'externals/course_list_admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['instructors'] = self.course.instructor_set.all()
        # context['topics'] = self.course.topic_set.all()
        return context


@method_decorator([login_required, admin_required], name='dispatch')
class AdminCourseDetailView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'take_course.html'
    pk_url_kwarg = 'course_pk'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.course = get_object_or_404(Course, pk=self.kwargs['course_pk'])
        context['instructors'] = self.course.instructor_set.all()
        # context['topics'] = self.course.topic_set.all()
        return context

