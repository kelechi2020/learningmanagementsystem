# coding=utf-8
from django import forms

from course.models import Course
from discussion.models import Post, Board
from .models import Topic


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'What is on your mind?'}),
        max_length=4000,
        help_text='The max length of the text is 4000.'
        )

    class Meta:
        model = Topic
        fields = ['subject', 'message']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]


class NewBoardForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.none())

    class Meta:
        model = Board
        fields = ('name', 'course','description')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('current_user')
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(creator=user)
