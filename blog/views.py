from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post
from django.utils import timezone


# Create your views here.
def post_list(request):
    return render(request, 'blog/post_list.html', {})


def post_list(requst):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(requst, 'blog/post_list.html', {'posts': posts})


def post_detail(requst, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(requst, 'blog/post_detail.html', {'post': post})


def post_new(requst):
    if requst.method == "POST":
        form = PostForm(requst.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = requst.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(requst, 'blog/post_edit.html', {'form': form})


def post_edit(requst, pk):
    post = get_object_or_404(Post, pk=pk)
    if requst.method == "POST":
        form = PostForm(requst.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = requst.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(requst, 'blog/post_edit.html', {'form': form})
