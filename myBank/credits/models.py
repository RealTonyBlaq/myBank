from django.db import models
from accounts.models import Account
from uuid import uuid4

# Create your models here.

TRANSACTION_STATUS = (
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed')
)


class Credit(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('inward_transfer', 'Inward_Transfer'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='credits')
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPES)
    amount = models.FloatField()
    transaction_id = models.UUIDField(default=uuid4, editable=False, unique=True)
    session_id = models.CharField(unique=True, blank=False, null=False)
    status = models.CharField(choices=TRANSACTION_STATUS, default='completed')
    narration = models.CharField(max_length=255, blank=True, null=True)
    # balance_before_transaction = models.DecimalField(max_digits=15, decimal_places=2)
    # balance_after_transaction = models.DecimalField(max_digits=15, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.date_created}"
