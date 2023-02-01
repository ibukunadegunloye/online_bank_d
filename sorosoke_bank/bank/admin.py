from django.contrib import admin
from .models import Savings_Account, Create_Account
from django.contrib.auth.models import User

# Register your models here.


admin.site.register(Savings_Account)
admin.site.register(Create_Account)
