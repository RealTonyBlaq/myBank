from django.db import models
from django.utils import timezone

# Create your models here.

class AccountOfficer(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40, default='', blank=True)
    phone_number = models.CharField(max_length=14, unique=True)
    official_email = models.EmailField(max_length=254, unique=True)
    employee_id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
