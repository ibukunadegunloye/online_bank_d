from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from account.forms import ExtendedUserForm
from .forms import Savings_Account_Form, Current_Account_Form
from account.models import ExtendedUser
from .models import CreateCurrentAccount, CreateSavingsAccount, Transfer
from django.shortcuts import get_object_or_404
from django.db import transaction
import decimal


# Create your views here.


def home(request):
    return render(request, 'bank/home.html',{})


def about(request):
    return render(request, 'bank/about.html', {})



def services(request):
    return render(request, 'bank/services.html', {})



def contact(request):
    return render(request, 'bank/contact.html', {})



@login_required
def savings_account(request):
    if request.method == 'POST':
        form = Savings_Account_Form(request.POST)
        if form.is_valid():
            savings_account = form.save(commit=False)
            savings_account.user = request.user
            savings_account.save()
            messages.success(request, f'Your Savings account has been created successfully')
            return redirect('home')
    else:
        form = Savings_Account_Form()
    return render(request, 'bank/savings_account.html', {'form': form})


@login_required
def current_account(request):
    if request.method == 'POST':
        form = Current_Account_Form(request.POST)
        if form.is_valid():
            current_account = form.save(commit=False)
            current_account.user = request.user
            current_account.save()
            messages.success(request, f'Your Current account has been created successfully')
            return redirect('home')
    else:
        form = Savings_Account_Form()
    return render(request, 'bank/current_account.html', {'form': form})



# #this is used to authenticate this view, a login decorator should be used later on
@login_required
def profile(request): 

    user_request = request.user
    #to get the users details
    current_user_id = request.user.id
    user = ExtendedUser.objects.get(id=current_user_id)
    return render(request, 'bank/profile.html',{'user':user})


# def account_information(request):
#     user = request.user
#     if user.is_authenticated:
#         #to get the user account
#         user = request.user
#         #THIS IS FOR ONLY CURRENT ACCOUNT, DO FOR SAVINGS TOO
#         accounts = CreateCurrentAccount.objects.filter(user=user)
#     return render(request, 'bank/account_information.html', {'accounts':accounts})


# Page that shows all the users savings accounts
@login_required
def savings(request):

    #to get the user account
    user = request.user
    accounts = CreateSavingsAccount.objects.filter(user=user)
    return render(request, 'bank/savings.html', {'accounts':accounts})


# Page that shows all the users current accounts
@login_required
def current(request):

    #to get the user account
    user = request.user
    accounts = CreateCurrentAccount.objects.filter(user=user)
    return render(request, 'bank/current.html', {'accounts':accounts})


#page to make transfers
@login_required
def transfer(request):
    user = request.user
    current_accounts = CreateCurrentAccount.objects.filter(user=user)
    savings_accounts = CreateSavingsAccount.objects.filter(user=user)
    context = {
        'current_accounts': current_accounts,
        'savings_accounts': savings_accounts,
    }

    if request.method == 'POST':
        from_account = request.POST.get('from_account')
        to_account = request.POST.get('to_account')
        amount = request.POST.get('amount')
        pin = request.POST.get('pin')
        print(request.POST)
        print('to_account: ', to_account)

        # Verify user's PIN
        if not user.check_pin(pin):
            print(pin)
            print(user.pin)
            print(user.check_pin(pin))
            messages.error(request, "Invalid PIN.")
            return redirect('transfer')


        # Check if the from and to accounts are the same
        if from_account == to_account:
            messages.error(request, "You cannot transfer money to the same account.")
            return redirect('transfer')

        # Retrieve host user by account number
        try:
            from_account = CreateSavingsAccount.objects.get(account_number=from_account)
        except CreateSavingsAccount.DoesNotExist:
            try:
                from_account = CreateCurrentAccount.objects.get(account_number=from_account)
            except CreateCurrentAccount.DoesNotExist: 
                messages.error(request, "Host account does not exist.")
                return redirect('transfer')

        # Retrieve the destination user by account number
        try:
            to_account = CreateCurrentAccount.objects.get(account_number=to_account)
        except CreateCurrentAccount.DoesNotExist:
            try:
                to_account = CreateSavingsAccount.objects.get(account_number=to_account)
            except CreateSavingsAccount.DoesNotExist: 
                messages.error(request, "Destination account does not exist.")
                return redirect('transfer')

        amount = decimal.Decimal(amount)

        with transaction.atomic():
            # Check if the sender has sufficient funds
            if from_account.account_balance < amount:
                messages.error(request, "Insufficient Balance.")
                return redirect('transfer')
            
            # Create a new Transfer object and save it
            transfer = Transfer(from_user=from_account.user, from_account_number=from_account, to_user=to_account.user, to_account_number=to_account, transfer_amount=amount)
            transfer.save()

            # Update the account balances for the sender and recipient
            from_account.account_balance -= amount
            to_account.account_balance += amount
            from_account.save()
            to_account.save()

            messages.success(request, "Transfer made successfully!")
            return redirect('transfer')

    return render(request, 'bank/transfer.html', context)



def search_account(request):
    account_number = request.GET.get('account_number')
    if len(account_number) == 12:
        savings_accounts = CreateSavingsAccount.objects.filter(account_number=account_number)
        current_accounts = CreateCurrentAccount.objects.filter(account_number=account_number)
        accounts = list(savings_accounts) + list(current_accounts)
        if accounts:
            data = {
                'found': True,
                'account_type': accounts[0].account_type,
                'account_balance': accounts[0].account_balance,
                'first_name': accounts[0].user.first_name,
                'last_name': accounts[0].user.last_name
            }
            return JsonResponse(data)
        else:
            data = {
                'found': False
            }
            return JsonResponse(data)
    return render(request, 'bank/search_account.html')
  






















