from django.urls import path
from .views import create_user, home, update_user, delete_user, get_user, list_users
from .address.views import get_address, create_address, update_address
from .next_of_kin.views import get_nok, create_nok, update_nok, delete_nok

urlpatterns = [
    path('create', create_user, name='create_user'),
    path('home', home, name='home'),
    path('update/<int:user_id>', update_user, name='update_user'),
    path('delete/<int:user_id>', delete_user, name='delete_user'),
    path('get/<int:user_id>', get_user, name='get_user'),
    path('list', list_users, name='list_users'),
    path('address/get/<int:user_id>', get_address, name='get_address'),
    path('address/create/<int:user_id>', create_address, name='create_address'),
    path('address/update/<int:user_id>', update_address, name='update_address'),
    path('nok/get/<int:user_id>', get_nok, name='get_nok'),
    path('nok/create/<int:user_id>', create_nok, name='create_nok'),
    path('nok/update/<int:user_id>', update_nok, name='update_nok'),
    path('nok/delete/<int:user_id>', delete_nok, name='delete_nok')
]
