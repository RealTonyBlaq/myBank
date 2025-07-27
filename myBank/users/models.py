from django.db import models
from staff.models import AccountOfficer

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40, default='', blank=True)
    phone_number = models.CharField(max_length=14)
    email = models.EmailField(max_length=254)
    state_of_origin = models.CharField(max_length=40)
    lga_of_origin = models.CharField(max_length=40, null=True, blank=True)
    date_of_birth = models.DateField()
    mother_maiden_name = models.CharField(max_length=40)
    BVN = models.CharField(max_length=11, unique=True, blank=True, null=True)
    NIN = models.CharField(max_length=11, blank=True, null=True, unique=True)
    title = models.CharField(max_length=5)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email}) - {self.phone_number})"

    @property
    def all_accounts(self):
        """
        Returns a list of accounts associated with the user.
        """
        return self.accounts.all() # type: ignore

    def to_dict(self):
        """
        Convert the User instance to a dictionary.
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'phone_number': self.phone_number,
            'address': self.address.to_dict() if self.address.exists() else None, # type: ignore
            'next_of_kin': self.next_of_kin.to_dict() if self.next_of_kin.exists() else None, # type: ignore
            'email': self.email,
            'state_of_origin': self.state_of_origin,
            'lga_of_origin': self.lga_of_origin,
            'date_of_birth': self.date_of_birth.isoformat(),
            'mother_maiden_name': self.mother_maiden_name,
            'BVN': self.BVN,
            'NIN': self.NIN,
            'title': self.title,
            'date_created': self.date_created.isoformat(),
            'date_updated': self.date_updated.isoformat(),
        }


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    kyc_done_by = models.ForeignKey(AccountOfficer, on_delete=models.CASCADE,
                                    related_name='verified_addresses', null=True)
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    local_government_area = models.CharField(max_length=40)
    nearest_bus_stop = models.CharField(max_length=40)
    house_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        """
        Convert the Address instance to a dictionary.
        """
        acc_officer = self.kyc_done_by.to_dict() if self.kyc_done_by else None
        return {
            'city': self.city,
            'state': self.state,
            'local_government_area': self.local_government_area,
            'nearest_bus_stop': self.nearest_bus_stop,
            'house_number': self.house_number,
            'street_name': self.street_name,
            'postal_code': self.postal_code,
            'kyc_done_by': acc_officer,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class NextOfKin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='next_of_kin')
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40, default='', blank=True)
    phone_number = models.CharField(max_length=14)
    email = models.EmailField(max_length=254, blank=True, null=True)
    relationship = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=40, blank=True, null=True)
    lga = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        """
        Convert the NextOfKin instance to a dictionary.
        """
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'phone_number': self.phone_number,
            'email': self.email,
            'relationship': self.relationship,
            'address': self.address,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
