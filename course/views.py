from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, UpdateView, ListView

from accounts.decorators import instructor_required
from course.models import Course, Topic


@method_decorator([login_required, instructor_required], name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    fields = ('title', 'slug', 'image', 'description', 'blob')
    template_name = 'course_add_form.html'

    def form_valid(self, form):
        course = form.save(commit=False)
        course.creator = self.request.user
        course.save()
        messages.success(self.request, 'The Course was created with success! Go ahead and add some quiz now.')
        return redirect('instructor:course_change_list')


@method_decorator([login_required, instructor_required], name='dispatch')
class CourseListView(ListView):
    model = Course
    ordering = ('title', )
    context_object_name = 'courses'
    template_name = 'course_change_list.html'

    def get_queryset(self):
        queryset = Course.objects.filter(creator=self.request.user)
        return queryset


@method_decorator([login_required, instructor_required], name='dispatch')
class CourseUpdateView(UpdateView):
    model = Course
    fields = ('title', 'slug', 'image', 'description', 'blob')
    context_object_name = 'quiz'
    template_name = 'course_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['course_name'] = self.get_object().title
        kwargs['pk']=self.kwargs['pk']
        return super().get_context_data(**kwargs)
    #
    def dispatch(self, request, *args, **kwargs):
        """





        """
        return super().dispatch(self, *args,**kwargs)

    def get_success_url(self):
        return reverse('instructor:course_change_list')


@method_decorator([login_required, instructor_required], name='dispatch')
class CourseDeleteView(DeleteView):
    model = Course
    context_object_name = 'quiz'
    template_name = 'quiz_delete_confirm.html'
    success_url = reverse_lazy('instructor:quiz_change_list')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.courses.all()


@method_decorator([login_required, instructor_required], name='dispatch')
class TopicCreateView(CreateView):
    model = Topic
    fields = ('topic_chapter', 'topic_title', 'topic_description', 'topic_duration')
    template_name = 'topic_add_form.html'

    # def form_valid(self, form):
    #     topic = form.save(commit=False)
    #     course.owner = self.request.user
    #     course.save()
    #     messages.success(self.request, 'The Course was created with success! Go ahead and add some quiz now.')
    #     return redirect('teachers:quiz_change', course.pk)


@method_decorator([login_required, instructor_required], name='dispatch')
class TopicListView(ListView):
    model = Topic
    ordering = ('title', )
    context_object_name = 'courses'
    template_name = 'course_change_list.html'

    def get_queryset(self):
        queryset = Course.objects.filter(creator=self.request.user)
        return queryset


@method_decorator([login_required, instructor_required], name='dispatch')
class TopicUpdateView(UpdateView):
    model = Topic
    fields = ('name', 'course', )
    context_object_name = 'quiz'
    template_name = 'quiz_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse('instructor:quiz_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, instructor_required], name='dispatch')
class TopicDeleteView(DeleteView):
    model = Topic
    context_object_name = 'quiz'
    template_name = 'quiz_delete_confirm.html'
    success_url = reverse_lazy('instructor:quiz_change_list')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()
