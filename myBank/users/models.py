from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40, default='', blank=True)
    phone_number = models.CharField(max_length=14)
    email = models.EmailField(max_length=254)
    state_of_origin = models.CharField(max_length=40)
    lga_of_origin = models.CharField(max_length=40, null=True, blank=True)
    date_of_birth = models.DateField()
    mother_maiden_name = models.CharField(max_length=40)
    BVN = models.CharField(max_length=11)
    NIN = models.CharField(max_length=11, blank=True, null=True)
    title = models.CharField(max_length=5)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # account_number = models.CharField(max_length=10, unique=True)
    # account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Boolean fields
    # is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email}) - {self.phone_number})"


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    city = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    local_government_area = models.CharField(max_length=40)
    nearest_bus_stop = models.CharField(max_length=40)
    house_number = models.CharField(max_length=10)


class NextOfKin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='next_of_kin')
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40, default='', blank=True)
    phone_number = models.CharField(max_length=14)
    email = models.EmailField(max_length=254, blank=True)
    relationship = models.CharField(max_length=20)
    address = models.TextField(blank=True)
