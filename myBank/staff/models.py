from django.db import models

# Create your models here.

class AccountOfficer(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40, default='', blank=True)
    phone_number = models.CharField(max_length=14)
    official_email = models.EmailField(max_length=254)
    employee_id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=50, null=True, blank=True)
