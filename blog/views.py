from django.shortcuts import get_object_or_404, render, redirect
from blog.forms import PostForm
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# Create your views here.

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    
    context = {
        'posts': posts,
    }
    return render(request, 'blog/post_list.html',  context)

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    context = {
        'posts': post,
    }
    return render(request, 'blog/post_list.html',  context)
