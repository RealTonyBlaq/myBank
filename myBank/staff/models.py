from django.db import models
from django.utils import timezone

# Create your models here.

class AccountOfficer(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.DO_NOTHING, related_name='account_officer', null=True, blank=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40, default='', blank=True)
    grade = models.CharField(max_length=20, null=True)
    role = models.CharField(max_length=30, null=True)
    phone_number = models.CharField(max_length=14, unique=True)
    official_email = models.EmailField(max_length=254, unique=True)
    employee_id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def to_dict(self):
        """
        Convert the AccountOfficer instance to a dictionary.
        """
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'grade': self.grade,
            'role': self.role,
            'phone_number': self.phone_number,
            'official_email': self.official_email,
            'employee_id': self.employee_id,
            'department': self.department,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active,
            'CABAL': self.accounts
        }
