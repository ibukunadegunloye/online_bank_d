from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import Savings_Account_Form, Create_Account_form
from .models import Create_Account
from django.contrib.auth.models import User
from .utils import account_number_generator

# Create your views here.


def home(request):
    user_request = request.user #this is used to authenticate this view, a login decorator should be used later on
    if user_request.is_authenticated:
        #to get the users username
        current_user_id = request.user.id
        user = User.objects.get(id=current_user_id)
        #to get the user account
        user = request.user
        account = Create_Account.objects.filter(user=user)
        all_account = Create_Account.objects.filter(user=user)
        return render(request, 'bank/home.html',{'users':user, 'account':account, 'all_account':all_account})
    else:
        messages.success(request, f'You have to login to view this page.')
        return redirect('login')


def savings_account(request):
    if request.method == 'POST':
        form = Savings_Account_Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your Savings account has been created succesfully')
            return redirect('home')
    else:
        #need this explained, want to know why this is passed to the form and how this dict is unloaded as a kwarg 
        form = Savings_Account_Form(initial={"user": request.user.id})
    return render(request, 'bank/savings_account.html', {'form': form, "account_number": account_number_generator()})

#dummy create account view
def create_account(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            form = Create_Account_form(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                account_number = form.cleaned_data['account_number']
                messages.success(request, f'Your Current account has been created succesfully!, Your account number is {account_number}')
                return redirect('home')
        else:
            form = Create_Account_form(initial={"user": request.user.id, "account_number": account_number_generator()})
        return render(request, 'bank/current_account.html', {'form': form})
    else:
        messages.success(request, f'You have to login to view this page.')
        return redirect('login')
