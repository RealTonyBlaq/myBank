from django.urls import path
from .views import info, create_account, change_dormant_status, change_PND_status, upgrade_account

urlpatterns = [
    path('query/<str:account_number>', info, name='account_info'),
    path('create/individual', create_account, name='create_account'),
    path('upgrade/<str:account_number>', upgrade_account, name='upgrade_account'),
    path('change_pnd/<str:account_number>', change_PND_status, name='change_pnd_status'),
    path('change_dormant/<str:account_number>', change_dormant_status, name='change_dormant_status'),
]
