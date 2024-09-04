from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('delete/<str:name>/', views.delete_task, name='delete'),
    path('update/<str:name>/', views.update_task, name='update'),
]
