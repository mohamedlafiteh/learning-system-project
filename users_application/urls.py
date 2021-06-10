
from django.urls import path
from . import  views

urlpatterns = [
    path('',views.home_page, name='home_page'),
    path('user_register/', views.user_register, name='user_register'),
    path('user_account_login/', views.user_account_login, name='user_account_login'),
    path('user_account_logout/', views.user_account_logout, name='user_account_logout'), 
]
