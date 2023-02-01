import time, random
from .models import Create_Account



def account_number_generator():
            x = "%0.12d" % random.randint(0,999999999999)
            return x



# def clean_account_number(self):
#         value = self.cleaned_data['account_number']
#         wed = Create_Account.objects.filter(account_number)