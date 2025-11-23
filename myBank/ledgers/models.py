from django.db import models
from accounts.models import Account

# Create your models here.

class Ledger(models.Model):
    transaction_id = models.CharField(blank=False, null=False)
    entry_id = models.AutoField(primary_key=True)
    status = models.CharField(null=False, blank=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='ledgers')
    entry_type = models.CharField(max_length=10, choices=[
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    ])
    amount = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    narration = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Ledger for {self.account} on {self.date_created}"
