from django.urls import path
from .views import create_officer, delete_officer, get_officer, get_all_officers, update_officer

urlpatterns = [
    path('create/', create_officer, name='create_officer'),
    path('delete/<int:officer_id>/', delete_officer, name='delete_officer'),
    path('get/<int:officer_id>/', get_officer, name='get_officer'),
    path('get_all/', get_all_officers, name='get_all_officers'),
    path('update/<int:officer_id>/', update_officer, name='update_officer'),
]
