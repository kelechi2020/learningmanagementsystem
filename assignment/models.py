from django.db import models

# Create your models here.
from accounts.models import User
from course.models import Course, Topic
from instructor.models import Instructor
from student.models import StudentProfile


class Assignment(models.Model):
    assignment_title = models.CharField(max_length=100, verbose_name="Assignment Title ")
    assign_description = models.CharField(max_length=100, verbose_name="Assignment Description")
    assignment_body = models .TextField(verbose_name="Assignment Content")
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(Instructor,on_delete=models.PROTECT)
    assignment_due_date = models.DateTimeField()
    course = models.ForeignKey(Course, verbose_name="Course name", on_delete=models.PROTECT)
    course_title = models.CharField(max_length=200, verbose_name="Course Title")
    topic = models.ForeignKey(Topic, verbose_name="Course Topic",on_delete=models.PROTECT)
    topic_title = models.CharField(max_length=200, verbose_name="Topic Title")

    def get_cuorse_and_topic_title(self):
        pass

    def __str__(self):
        return self.assignment_title


class AssignmentAttachment(models.Model):
    name = models.CharField(max_length=200, verbose_name="File Name")
    file_description = models.CharField(max_length=200, verbose_name="Course Title")
    file = models.FileField(upload_to='files/')
    uploaded_by = models.ForeignKey(User,on_delete=models.PROTECT)

    def get_file_name(self):
        pass


class SubmittedAssignmentFiles(AssignmentAttachment):
    """
    IN the case if there are specific attributes that could be added later
    """
    pass


class SubmittedAssignment(models.Model):
    assignment = models.ForeignKey(Assignment,on_delete=models.PROTECT)
    submission_date = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(StudentProfile,on_delete=models.PROTECT)
    assignment_body = models.TextField()
    attached_files = models.ForeignKey(SubmittedAssignmentFiles,on_delete=models.PROTECT)


class AssignmentReview(models.Model):
    submitted_assignment = models.ForeignKey(SubmittedAssignment,on_delete=models.PROTECT)
    review_date = models.DateTimeField()
    review = models.CharField(max_length=200)
    rating = models.IntegerField(blank=True, null=True)

