# coding=utf-8
from django.contrib import admin
from accounts.models import User
from course.models import Course, Topic
from discussion.models import Board, Topic as DiscussionTopic, Post
from student.models import StudentProfile, StudentTakenQuiz, StudentCourses, StudentAnswer

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(StudentProfile)
admin.site.register(StudentAnswer)
admin.site.register(StudentTakenQuiz)
admin.site.register(StudentCourses)
admin.site.register(Board)
admin.site.register(DiscussionTopic)
admin.site.register(Post)



