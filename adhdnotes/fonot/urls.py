from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('create_file/', views.create_file, name='create_file'),
    path('file_list/', views.file_list, name='file_list'),
    path('edit_file/<int:file_id>/', views.edit_file, name='edit_file'),
]
