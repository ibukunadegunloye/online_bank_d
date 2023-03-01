from django import forms
from django.contrib.auth.models import User
from .models import CreateCurrentAccount, CreateSavingsAccount
from account.models import ExtendedUser




class Savings_Account_Form(forms.ModelForm):
    
    account_balance = forms.CharField()
    class Meta:
        model = CreateSavingsAccount
        fields = []
        widgets = {
            'first_name': forms.TextInput(attrs={'readonly': 'readonly'})
        }
        
class Current_Account_Form(forms.ModelForm):
    
    account_balance = forms.CharField()
    class Meta:
        model = CreateCurrentAccount
        fields = []
        widgets = {
            'first_name': forms.TextInput(attrs={'readonly': 'readonly'})
        }
        

    



# class Create_Account_form(forms.ModelForm):

#     class Meta:
#         model = CreateSavingsAccount
#         account_number = forms.UUIDField()
#         fields = ['account_type','account_number', 'account_balance' , 'initial_deposit_amount']
#         widgets = {
#             'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
#             'funds': forms.HiddenInput(),
#             'account_number': forms.TextInput(attrs={'readonly': 'readonly'})
#         }

        

#    when a profile is created , there should be an optional button 

#    saving or curent and based on what the person picks an account of their

#    choice is created, not: current account requires you have a savings CreateAccount

#    so in the logic, whenn teh user creation form is submitted and saved to a variable

#    depending on the choice of account, the particular user is then tied to an account

#    instance of their choice. note you should also make it madatory that a savings exists for a current to exist.