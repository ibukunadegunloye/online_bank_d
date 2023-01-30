from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import Savings_Account_Form,Curren_Account_Form

# Create your views here.


def home(request):
    user = request.user
    if user.is_authenticated:
        return render (request, 'bank/home.html', {})
    else:
        messages.success(request, f'You have to login to view this page.')
        return redirect ('login')

def savings_account(request):
    if request.method == 'POST':
        form = Savings_Account_Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your Savings account has been created succesfully')
            return redirect ('home')
    else:
        form = Savings_Account_Form()
    return render (request, 'bank/savings_account.html', {'form':form})



def current_account(request):
    if request.method == 'POST':
        form = Curren_Account_Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your Current account has been created succesfully')
            return redirect ('home')
    else:
        form = Curren_Account_Form()
    return render (request, 'bank/current_account.html', {'form':form})

