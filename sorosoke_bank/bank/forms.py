from django import forms
from django.contrib.auth.models import User

from .models import Savings_Account, Current_Account


class Savings_Account_Form(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=None, widget=forms.HiddenInput())
    class Meta:
        model = Savings_Account
        fields = ['user', 'savings_rubbish', 'account_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].queryset = User.objects.all()



class Curren_Account_Form(forms.ModelForm):
    
    class Meta:
        model = Current_Account
        fields = ['current_rubbish','account_number']