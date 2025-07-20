from django.urls import path
from .views import info, create_account

urlpatterns = [
    path('query/<str:account_number>', info, name='account_info'),
    path('create/individual', create_account, name='create_account'),
]
