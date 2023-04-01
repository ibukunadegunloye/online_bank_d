from django.db import models
from django.contrib.auth.models import User
from account.models import ExtendedUser 
from django.contrib import messages
from .utils import initial_deposit_minimum
import random
import uuid
from django.utils import timezone



# Create your models here.

class CreateSavingsAccount(models.Model):

    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=255, default='Savings Account', null=False)
    account_number = models.CharField(primary_key=True, max_length=12, editable=False)
    account_balance = models.DecimalField(max_digits=20, decimal_places=2, default=1000000.00)
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
        return f" {self.user.first_name} ||{self.account_number}"



initial_deposit_amount = models.DecimalField(max_digits=20, null=False, decimal_places=2, validators=[initial_deposit_minimum])

 # additional fields for profile information
    #house address,  means of ID, Utility bill,
    #current - + two active current account users to refer you


class CreateCurrentAccount(models.Model):

    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=255, default='Current Account', null=False)
    account_number = models.CharField(primary_key=True, max_length=12, editable=False)
    account_balance = models.DecimalField(max_digits=20, decimal_places=2, default=1000000.00)
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
        return f" {self.user.first_name} || {self.account_number}"


class Transfer(models.Model):

    transfer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, related_name='from_user', null=True)
    to_user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, related_name='to_user', null=True)
    from_account_number = models.CharField(max_length=12, editable=False, null=True)
    to_account_number = models.CharField(max_length=12, editable=False, null=True)
    transfer_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    transfer_date = models.DateTimeField(auto_now_add=True)
    transfer_description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.transfer_id} || {self.from_account_number} || {self.to_account_number}"



class Credit(models.Model):

    credit_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dest_account = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, related_name='dest_account', null=True)
    dest_account_number = models.CharField(max_length=12, editable=False, null=True)
    credit_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    credit_source = models.CharField(max_length=50, null=True)
    credit_time = models.DateTimeField(auto_now_add=True)
    credit_description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.credit_id} || {self.credit_amount} || {self.dest_account_number}"


class TransferEmailLog(models.Model):
    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, null=True, related_name='transfer_email_log')
    subject = models.CharField(max_length=100)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer Email Log for {self.user.first_name} {self.user.last_name}"


class CreditEmailLog(models.Model):
    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, null=True, related_name='credit_email_log')
    subject = models.CharField(max_length=100)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Credit Email Log for {self.user.first_name} {self.user.last_name}"




class PinResetToken(models.Model):
    user = models.OneToOneField(ExtendedUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    expiry_time = models.DateTimeField()
    
    def is_valid(self):
        return timezone.now() < self.expiry_time
