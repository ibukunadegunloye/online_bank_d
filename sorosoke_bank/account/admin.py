from django.contrib import admin
from .models import ExtendedUser, AccountVerificationEmailLog, WelcomeEmailLog


# Register your models here.


admin.site.register(ExtendedUser)
admin.site.register(AccountVerificationEmailLog)
admin.site.register(WelcomeEmailLog)