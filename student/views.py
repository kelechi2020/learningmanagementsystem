# coding=utf-8
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from accounts.decorators import student_required
from course.models import Course
from quiz.forms import TakeQuizForm
from quiz.models import Quiz
from student.models import StudentTakenQuiz, StudentProfile


@method_decorator([login_required], name='dispatch')
class CourseListView(ListView):
    """
        Returns a list of all available courses on the platform
    """
    model = Course
    ordering = ('title', )
    context_object_name = 'courses'
    template_name = 'course_change_list.html'

    def get_queryset(self):
        """
        Returns queryset to be used for displaying data on template
        :return:
        """
        student = get_object_or_404(StudentProfile, user=self.request.user).course.values('title')
        queryset = Course.objects.exclude(studentprofile__course__title__in=student)
        return queryset


@login_required
@student_required
def course_registration(request, course_pk):
    """
    Handles Student Course Registration
    Returns a context containing list of courses registered by student and  a list of
    students un-registered courses.
    Also ensures that a student cannot register a course twice
    :param request:
    :param course_pk:
    :return:
    """
    course = get_object_or_404(Course, pk=course_pk)
    student = get_object_or_404(StudentProfile, user=request.user)
    student_registered_courses = student.course.all()
    unregistered_courses = Course.objects.exclude(studentprofile__course__in=student_registered_courses)

    if course in student_registered_courses:
        messages.error(request, "This Course {0} has been registered ".format(course.title))
        return render(request, 'student_registered_courses.html', {'student_registered_courses':student_registered_courses, \
                                                                   'unregistered_courses':unregistered_courses})
    #register student to course
    student.course.add(course)
    messages.success(request, "the course {0} was successfully added".format(course.title))
    return render(request, 'student_registered_courses.html', {'student_registered_courses': student_registered_courses, \
                                                                   'unregistered_courses':unregistered_courses})







@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/students/quiz_list.html'

    def get_queryset(self):
        student = self.request.user
        student_interests = student.interests.values_list('pk', flat=True)
        taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(subject__in=student_interests) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = StudentTakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'classroom/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset


@login_required
@student_required
def take_quiz(request, pk):

    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student

    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'students/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    print("we still have un answered questions")
                    return redirect('student:take_quiz', pk)
                else:
                    print("here")
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    print(correct_answers)
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    StudentTakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
                    return redirect('student:quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'classroom/students/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })
