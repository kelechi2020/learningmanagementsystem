from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView
from accounts.decorators import instructor_required
from course.models import Course, Topic
from instructor.models import Instructor
from student.models import StudentProfile


@method_decorator([login_required, instructor_required], name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    fields = ('title', 'slug', 'image', 'description', 'blob')
    template_name = 'course_add_form.html'

    def form_valid(self, form):
        course = form.save(commit=False)
        course.creator = self.request.user
        instructor = Instructor.objects.get(user=self.request.user)
        course.save()
        instructor.course.add(course)
        messages.success(self.request, 'The Course was created with success! Go ahead and add some quiz now.')
        return redirect('instructor:course_change_list')


@method_decorator([login_required], name='dispatch')
class CourseListView(ListView):
    model = Course
    ordering = ('title', )
    context_object_name = 'courses'
    template_name = 'course_change_list.html'

    def get_queryset(self):
        queryset = Course.objects.filter(creator=self.request.user)
        return queryset

@method_decorator([login_required], name='dispatch')
class CourseDetailView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = 'take_course.html'
    pk_url_kwarg = 'course_pk'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instructors'] = self.course.instructor_set.all()
        context['topics'] = self.course.topic_set.all()
        return context

    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, pk=self.kwargs['course_pk'])
        student_registered_courses = get_object_or_404(StudentProfile, user=request.user).course.all()
        unregistered_courses = Course.objects.exclude(studentprofile__course__in=student_registered_courses)

        if self.course in student_registered_courses:
            return super().dispatch(request)
        else:
            messages.error(request, "You have not registered this course{0} ".format(self.course.title))
            return render(request, 'student_registered_courses.html',
                          {'student_registered_courses': student_registered_courses, \
                           'unregistered_courses': unregistered_courses})
        # register student to course




@method_decorator([login_required, instructor_required], name='dispatch')
class CourseUpdateView(UpdateView):
    model = Course
    fields = ('title', 'slug', 'image', 'description', 'blob')
    context_object_name = 'quiz'
    template_name = 'course_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['course_name'] = self.get_object().title
        kwargs['pk'] =self.kwargs['pk']
        return super().get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        Overiding the dispatch method to ensure that only the authr of a course can change it
        """
        obj = self.get_object()
        if obj.creator != self.request.user:
            messages.error(self.request, "You cant edit this couurse as you are not the author")
            return redirect('instructor:course_change_list')
        return super().dispatch(request)

    def get_success_url(self):
        return reverse('instructor:course_change_list')


@method_decorator([login_required, instructor_required], name='dispatch')
class CourseDeleteView(DeleteView):
    model = Course
    context_object_name = 'quiz'
    template_name = 'course_delete_confirm.html'
    success_url = reverse_lazy('instructor:quiz_change_list')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The course %s was deleted with success!' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.courses.all()

    def dispatch(self, request, *args, **kwargs):
        """
        Overiding the dispatch method to ensure that only the authr of a course can change it
        """
        obj = self.get_object()
        if obj.creator != self.request.user:
            messages.error(self.request, "You cant delete this couurse as you are not the author")
            return redirect('instructor:course_change_list')
        return super().dispatch(request)


@method_decorator([login_required, instructor_required], name='dispatch')
class TopicCreateView(CreateView):
    model = Topic
    fields = ('topic_chapter', 'topic_title', 'topic_description', 'topic_duration')
    template_name = 'topic_add_form.html'

    def form_valid(self, form):
        topic = form.save(commit=False)
        course = Course.objects.get(pk=self.kwargs['course_pk'])
        if self.request.user != course.creator:
            messages.error(self.request, 'You are now alowed to add topics to a course you did not author')
            return redirect('instructor:topic_change_list')
        topic.topics_course = course
        topic.save()
        messages.success(self.request, 'The Topic was created with success! Go ahead and add some quiz now.')
        return redirect('instructor:topic_change_list',)


@method_decorator([login_required, instructor_required], name='dispatch')
class TopicListView(ListView):
    model = Topic
    ordering = ('title', )
    context_object_name = 'topics'
    template_name = 'topic_change_list.html'

    def get_queryset(self):
        queryset = Topic.objects.filter(topics_course__creator=self.request.user)
        return queryset


@method_decorator([login_required, instructor_required], name='dispatch')
class TopicUpdateView(UpdateView):
    model = Topic
    fields = ('name', 'course', )
    context_object_name = 'quiz'
    template_name = 'topic_change_form.html'

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

    def dispatch(self, request, *args, **kwargs):
        """
        Overiding the dispatch method to ensure that only the author of a topic can change it
        """
        obj = self.get_object()
        if obj.creator != self.request.user:
            messages.error(self.request, "You cant edit this Topic as you are not the author")
            return redirect('instructor:course_change_list')
        return super().dispatch(request)


@method_decorator([login_required, instructor_required], name='dispatch')
class TopicDeleteView(DeleteView):
    model = Topic
    context_object_name = 'quiz'
    template_name = 'quiz_delete_confirm.html'
    success_url = reverse_lazy('instructor:quiz_change_list')

    def delete(self, request, *args, **kwargs):
        topic = self.get_object()
        messages.success(request, 'The Topic %s was deleted with success!' % topic.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()

    def dispatch(self, request, *args, **kwargs):
        """
        Overriding the dispatch method to ensure that only the author of a topic can change it
        """
        obj = self.get_object()
        if obj.creator != self.request.user:
            messages.error(self.request, "You cant delete this topic as you are not the author")
            return redirect('instructor:course_change_list')
        return super().dispatch(request)