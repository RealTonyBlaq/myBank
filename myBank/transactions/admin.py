from django.contrib import admin
from .models import Credit, Debit, Ledger

# Register your models here.

admin.site.register([Credit, Debit, Ledger])
