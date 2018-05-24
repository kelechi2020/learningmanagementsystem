from django.contrib import admin

# Register your models here.
from accounts.models import User,GuestProfile
from course.models import Course,Topic
from discussion.models import Board, Topic as DiscussionTopic, Post
from instructor.models import Instructor
from student.models import StudentProfile,StudentTakenQuiz,StudentCourses
from teaching_assistant.models import TeachingAssistant
from quiz.models import Quiz,Question ,Answer ,StudentAnswer
from assignment.models import Assignment,SubmittedAssignment,AssignmentAttachment,AssignmentReview \
    ,SubmittedAssignmentFiles

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(Instructor)
admin.site.register(StudentProfile)
admin.site.register(TeachingAssistant)
admin.site.register(Assignment)
admin.site.register(SubmittedAssignmentFiles)
admin.site.register(SubmittedAssignment)
admin.site.register(StudentAnswer)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(AssignmentAttachment)
admin.site.register(AssignmentReview)
admin.site.register(StudentTakenQuiz)
admin.site.register(StudentCourses)
admin.site.register(GuestProfile)
admin.site.register(Board)
admin.site.register(DiscussionTopic)
admin.site.register(Post)



