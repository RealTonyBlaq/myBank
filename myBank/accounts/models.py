from django.db import models
from users.models import User
from staff.models import AccountOfficer
from .helper_functions import calculate_account_balance

# Create your models here.

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_officer = models.ForeignKey(AccountOfficer, on_delete=models.SET_NULL,
                                        null=True, blank=True, related_name='accounts')
    account_number = models.CharField(max_length=10, unique=True)
    account_level = models.CharField(default='1', choices=[
        ('1', 'Level 1'),
        ('2', 'Level 2'),
        ('3', 'Level 3'),
    ])
    CLASS = models.JSONField(blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # Boolean fields
    is_PND_active = models.BooleanField(default=False)
    is_dormant = models.BooleanField(default=False)


    @property
    def balance(self):
        """
        Calculate the account balance using the helper function.
        """
        return calculate_account_balance(self)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.account_number}"
