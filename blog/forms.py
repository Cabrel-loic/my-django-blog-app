from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from django.contrib.auth import get_user_model

class PostForm(forms.ModelForm):
       
       class Meta:
           model = Post
           fields = ['title', 'content', 'image']
   
class CommentForm(forms.ModelForm):
      class Meta:
            model = Comment
            fields = ['body']


class CustomUserCreationForm(UserCreationForm):
      email = forms.EmailField(required = True)
      class Meta:
            model = get_user_model()
            # model = User
            fields = ('username', 'email', 'password1', 'password2')

