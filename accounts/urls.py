from django.urls import path
from .views import *

urlpatterns = [
    path('users/',user_view, name='users'),
    path('users/create/',create_user_view, name='create_users'),
    path('users/edit/',edit_user_view, name='edit_users'),
]