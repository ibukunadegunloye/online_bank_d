from django import forms
from .models import Savings_Account, Current_Account


class Savings_Account_Form(forms.ModelForm):

    class Meta:
        model = Savings_Account
        fields = ['savings_rubbish','account_number']

class Curren_Account_Form(forms.ModelForm):
    
    class Meta:
        model = Current_Account
        fields = ['current_rubbish','account_number']