from django.urls import path
from blog.views import *

urlpatterns = [
       path('', post_list, name='post_list'),
       path('post/<int:pk>/',post_detail, name='post_detail'),
       path('post/<int:pk>/edit/', post_edit, name='post_edit'),
       path('post/<int:pk>/delete/', post_delete, name='post_delete'),
       path('create-post/', post_create, name='post_create'),
   ]
   