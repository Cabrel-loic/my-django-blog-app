from django.contrib import admin
from django.urls import include, path
from blog.views  import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    #path('register/', register_view, name="register"),
    #path('login/', login_view, name="login"),
    #path('logout/', logout_view, name="logout"),
    
]
