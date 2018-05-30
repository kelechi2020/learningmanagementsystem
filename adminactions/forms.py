from django import forms
from course.models import Course
from instructor.models import Instructor


class AdminCourseAssignmentForm(forms.ModelForm):
    instructor = forms.ModelChoiceField(queryset=Instructor.objects.none(), required=True)
    course = forms.ModelChoiceField(queryset=Course.objects.none(), required=True)

    class Meta:
        model = Instructor
        fields = ('instructor', 'course')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()
        self.fields['instructor'].queryset = Instructor.objects.all()
