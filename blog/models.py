from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Post(models.Model):
    title = models.CharField (max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField (auto_now_add=True)
    updated_at = models.DateTimeField (auto_now=True)
    
    def __str__(self):
        return str(self.title)
