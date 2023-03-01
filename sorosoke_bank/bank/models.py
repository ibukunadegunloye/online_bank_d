from django.db import models
from django.contrib.auth.models import User
from account.models import ExtendedUser 
from django.contrib import messages
from .utils import initial_deposit_minimum
import random
import uuid




# Create your models here.

class CreateSavingsAccount(models.Model):

    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=255, default='Savings Account', null=False)
    account_number = models.CharField(primary_key=True, max_length=12, editable=False)
    account_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    account_created_at = models.DateTimeField(auto_now_add=True)
    account_updated_at = models.DateTimeField(auto_now=True)

    def account_number_generator(self):
        x = "%0.12d" % random.randint(0,999999999999)
        while CreateSavingsAccount.objects.filter(account_number=x).exists() and CreateCurrentAccount.objects.filter(account_number=x).exists():
            x = self.account_number_generator()
        return x

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.account_number_generator()
        super().save(*args, **kwargs)

    def __str__(self):
        return f" {self.user.first_name} ||{self.account_number} || {self.account_type}"



initial_deposit_amount = models.DecimalField(max_digits=20, null=False, decimal_places=2, validators=[initial_deposit_minimum])

 # additional fields for profile information
    #house address,  means of ID, Utility bill,
    #current - + two active current account users to refer you


class CreateCurrentAccount(models.Model):

    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=255, default='Current Account', null=False)
    account_number = models.CharField(primary_key=True, max_length=12, editable=False)
    account_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    account_created_at = models.DateTimeField(auto_now_add=True)
    account_updated_at = models.DateTimeField(auto_now=True)

    def account_number_generator(self):
        x = "%0.12d" % random.randint(0,999999999999)
        while CreateCurrentAccount.objects.filter(account_number=x).exists() and CreateSavingsAccount.objects.filter(account_number=x).exists():
            x = self.account_number_generator()
        return x

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.account_number_generator()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.account_number} || {self.account_type}"


class Transfer(models.Model):

    transfer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, related_name='from_user', null=True)
    to_user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, related_name='to_user', null=True)
    from_account_number = models.CharField(max_length=12, editable=False, null=True)
    to_account_number = models.CharField(max_length=12, editable=False, null=True)
    transfer_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    transfer_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_account_number} || {self.to_account_number}"