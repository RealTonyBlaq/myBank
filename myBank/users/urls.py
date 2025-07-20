from django.urls import path
from .views import create_user, home

urlpatterns = [
    path('create', create_user, name='create_user'),
    path('home', home, name='home')
]
