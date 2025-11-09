from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', LoginView.as_view(template_name='userapp/login.html'), name='user_home'),  # handles /user
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='userapp/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
]
