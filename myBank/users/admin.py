from django.contrib import admin
from .models import User, Address, NextOfKin

admin.site.register([User, Address, NextOfKin])
