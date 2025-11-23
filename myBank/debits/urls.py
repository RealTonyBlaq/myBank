from django.urls import path
from .views import outflow


urlpatterns = [
    path('', outflow, name="outflow")
]
