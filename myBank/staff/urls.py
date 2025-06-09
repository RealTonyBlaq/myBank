from django.urls import path
from .views import create_officer

urlpatterns = [
    path('', create_officer, name='create_officer')
]
