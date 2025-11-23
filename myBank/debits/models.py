from django.db import models
from accounts.models import Account
from uuid import uuid4

# Create your models here.


TRANSACTION_STATUS = (
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed')
)


class Debit(models.Model):
    TRANSACTION_TYPES = (
        ('withdrawal', 'Withdrawal'),
        ('outward_transfer', 'Outward_Transfer'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='debits')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.FloatField()
    transaction_id = models.UUIDField(default=uuid4(), editable=False, unique=True)
    status = models.CharField(choices=TRANSACTION_STATUS, default='pending')
    narration = models.CharField(max_length=255, blank=True, null=True)
    balance_before_transaction = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=15, decimal_places=2)
    beneficiary_account_number = models.CharField(max_length=10, blank=True, null=True)
    beneficiary_bank = models.CharField(max_length=50, blank=True, null=True)
    beneficiary_name = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.date_created}"
