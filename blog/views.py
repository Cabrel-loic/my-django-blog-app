from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from .forms import PostForm, CommentForm, CustomUserCreationForm
from .models import Post

# Create your views here.

class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy('login')
    success_message = 'Your account has been created successfully. You can now login.'

    def form_valid(self, form):
        #additional processes can be added here like sending a confirmation email etc.

        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'template/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'template/logout.html'


def post_list(request):
    query = request.GET.get("q")
    posts = Post.objects.all().order_by('-created_at')
    if query:
        posts = Post.objects.filter(Q(title__icontains = query) | Q(content__icontains = query)
                                    )
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': posts,
        "user": request.user,
        'page_obj': page_obj,
        'query': query
    }
    return render(request, 'blog/post_list.html',  context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            new_comment = form.save(commit = False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('post_detail', pk = post.pk)
    else:
        form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'blog/post_details.html', context)
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_list')


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk =post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Check if the user is the author of the post
    if post.author != request.user:
        return redirect('post_list', pk=post.pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit = False)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Check if the user is the author of the post
    if post.author != request.user:
        return redirect('post_list')
    
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    context = {
        'posts': post,
    }
    return render(request, 'blog/post_list.html', context)
