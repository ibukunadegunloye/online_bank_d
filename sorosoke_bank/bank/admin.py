from django.contrib import admin
from .models import CreateCurrentAccount, CreateSavingsAccount, Transfer
from django.contrib.auth.models import User, Group

# Register your models here.


admin.site.unregister(Group)
admin.site.register(CreateCurrentAccount)
admin.site.register(CreateSavingsAccount)
admin.site.register(Transfer)