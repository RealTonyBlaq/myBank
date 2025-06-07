from django.db import models
from myBank.users.models import User

# Create your models here.


# Individual Account Types
class SavingsAccount(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    account_number = models.CharField(max_length=10, unique=True)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    account_level = models.CharField(default='1', choices=[
        ('1', 'Level 1'),
        ('2', 'Level 2'),
        ('3', 'Level 3'),
    ])
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # Boolean fields
    is_PND_active = models.BooleanField(default=False)
    is_dormant = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.account_number} ({self.account_balance})"


class CurrentAccount(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='current_account')
    account_number = models.CharField(max_length=10, unique=True)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # Boolean fields
    is_PND_active = models.BooleanField(default=False)
    is_dormant = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.account_number} ({self.account_balance})"
