# coding=utf-8
from django.db import models
from accounts.models import User
from course.models import Course
from quiz.models import Answer


class StudentProfile(models.Model):
    """
    Used to represent fields specific to the student user
    it's user field has a one to one relationship with the  User class
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    school_number = models.CharField(max_length=20, null=True, blank=True)
    photo = models.FileField(upload_to='tutor', null=True, blank=True)
    designation = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    student_quizzes = models.ManyToManyField('quiz.Quiz', through='StudentTakenQuiz')
    course = models.ManyToManyField(Course)

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    class Meta:
        verbose_name_plural = 'Student'

    def __str__(self):
        return self.user.username


class StudentCourses(models.Model):
    student = models.ForeignKey(StudentProfile, null=True, on_delete=models.CASCADE)
    student_course = models.ManyToManyField(Course)

    class Meta:
        verbose_name_plural = 'Student Courses'


class StudentTakenQuiz(models.Model):
    student = models.ForeignKey('student.StudentProfile', on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey('quiz.Quiz', on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey('quiz.Answer', on_delete=models.CASCADE, related_name='+')