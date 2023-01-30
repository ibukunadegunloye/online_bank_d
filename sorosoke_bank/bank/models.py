from django.db import models
from django.contrib.auth.models import User
import time, random

# Create your models here.

def account_number_generator():
    present_account_number_list = [0]
    for num in present_account_number_list:
        x = "%0.12d" % random.randint(0,999999999999)
        if x != num:
            present_account_number_list.append(x)
            return int(x)
        else:
            account_number_generator()

class Savings_Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    savings_rubbish = models.CharField(max_length=30)
    account_number = models.PositiveBigIntegerField(primary_key=True, default=0)

    

class Current_Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_rubbish = models.CharField(max_length=30, default="")
    account_number = models.PositiveBigIntegerField(primary_key=True, default=account_number_generator())


