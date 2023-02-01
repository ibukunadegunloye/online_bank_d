from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.contrib import messages
import datetime


# Create your models here.

class Savings_Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    savings_rubbish = models.CharField(max_length=30)
    account_number = models.PositiveBigIntegerField(primary_key=True, default=0)

    def __str__(self):
        return str(self.user) + ' | ' + str(self.account_number) 

    

class Create_Account(models.Model):
    account_type_choices = [
        ('Current_Account','Current Account'),
        ('Savings_Account','Savings Account')]
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=datetime.date.today)
    nationality = CountryField(default='Nigeria')
    account_type = models.CharField(max_length=255, choices=account_type_choices)
    account_number = models.PositiveBigIntegerField(primary_key=True, default=0)
    funds = models.PositiveBigIntegerField(default=float(0.00))

    
   
   
   
    # additional fields for profile information
    #house address,  means of ID, Utility bill,
    #current - + two active current account users to refer you

    def __str__(self):
        return self.account_type



