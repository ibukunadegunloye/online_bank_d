from django import forms
from django.contrib.auth.models import User
from .models import Savings_Account, Create_Account
import random


class Savings_Account_Form(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=None, widget=forms.HiddenInput())
    class Meta:
        model = Savings_Account
        fields = ['user', 'savings_rubbish', 'account_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].queryset = User.objects.all()
    
    



class Create_Account_form(forms.ModelForm):
    
    class Meta:
        model = Create_Account
        fields = ['account_type','account_number','nationality','date_of_birth','funds']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'funds': forms.HiddenInput()
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['account_number'].initial = self.account_number_generator()

        def account_number_checker(self):
            account_number = self.account_number_generator()
            while Create_Account.objects.filter(account_number=account_number).exists():
                account_number = self.account_number_generator()
            return account_number
    
        def account_number_generator():
            x = "%0.12d" % random.randint(0,999999999999)
            return x


   