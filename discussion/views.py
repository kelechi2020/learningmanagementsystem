from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from accounts.decorators import instructor_required
from course.models import Course
from discussion.forms import NewTopicForm, PostForm, NewBoardForm
from discussion.models import Board, Post, Topic


def discussion_home(request):
    boards = Board.objects.all()
    return render(request, 'discussion_home.html', {'boards': boards})


@method_decorator([login_required, instructor_required], name='dispatch')
class BoardCreateView(CreateView):
    """

    """
    form_class = NewBoardForm
    template_name = 'create_discussion_board.html'
    success_url = reverse_lazy('discussion_home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object, 'current_user': self.request.user})
            return kwargs

    def form_valid(self, form):
        board = form.save(commit=False)
        course = Course.objects.filter(creator=self.request.user).first()
        print(self.request.user, course.creator)
        if self.request.user != course.creator:
            messages.error(self.request, 'You are now allowed to create discussions for a course you did not author')
            return redirect('')
        board.created_by = self.request.user
        board.save()
        messages.success(self.request, 'The Board was created with success! Go ahead and add some Topics  now.')
        return redirect('discussion_home')



def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    print(type(topic))
    return render(request, 'topic_posts.html', {'topic': topic, 'board_pk': pk, 'topic_pk': topic_pk})

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})

