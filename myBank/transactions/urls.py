from django.urls import path
from .views import inflow


urlpatterns = [
    path('receive', inflow, name='inflow'),
]
