from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from account.forms import ExtendedUserForm
from .forms import Savings_Account_Form, Current_Account_Form
from account.models import ExtendedUser
from .models import CreateCurrentAccount, CreateSavingsAccount, Transfer, Credit, CreditEmailLog, TransferEmailLog
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.humanize.templatetags import humanize
import decimal
import os


# Create your views here.


def home(request):
    return render(request, 'bank/home.html',{})


def about(request):
    return render(request, 'bank/about.html', {})



def services(request):
    return render(request, 'bank/services.html', {})



def contact(request):
    return render(request, 'bank/contact.html', {})



def send_credit_alert(dest_account, amount, credit_source, credit_time, credit_date, credit_id, description):
    user = dest_account.user
    subject = f"SSBeNS Credit Alert: N{humanize.intcomma(amount)} credited to your account"

    # Render the HTML content using a template
    html_content = render_to_string('bank/credit_alert_by_self.html', {
        'user': dest_account,
        'amount': amount,
        'credit_source': credit_source,
        'description': description,
        'credit_time': credit_time,
        'credit_date': credit_date,
        'credit_id': credit_id
    })

    # Create a plain text version of the email
    text_content = render_to_string('bank/credit_alert_by_self.txt', {
        'user': user,
        'amount': amount,
        'credit_source': credit_source,
        'description': description,
        'credit_time': credit_time,
        'credit_date': credit_date,
        'credit_id': credit_id
    })

    # Create the email message object and attach the HTML content as an alternative
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(subject, text_content, from_email, [dest_account.user.email])
    msg.attach_alternative(html_content, "text/html")

    # Send the email
    msg.send()

    # Log the email
    CreditEmailLog.objects.create(
        user=user,
        subject=subject,
        body=text_content,
    )


def send_transfer_debit_alert(from_account, to_account, amount, transfer_date, transfer_time, transfer_id, description):
    user =from_account.user
    subject = f"SSBeNS Debit Alert: N{humanize.intcomma(amount)} debited from your account"
   
    # Render the HTML content using a template
    html_content = render_to_string('bank/debit_alert.html', {
        'user': from_account,
        'amount': amount,
        'reciever': to_account,
        'description': description,
        'transfer_time': transfer_time,
        'transfer_date': transfer_date,
        'transfer_id': transfer_id
    })

    # Create a plain text version of the email
    text_content = render_to_string('bank/debit_alert.txt', {
    'user': from_account,
    'amount': amount,
    'transfer_date': transfer_date,
    'transfer_time': transfer_time,
    'reciever': to_account,
    'transfer_id': transfer_id,
    'description': description,
    })

    # Create the email message object and attach the HTML content as an alternative
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(subject, text_content, from_email, [from_account.user.email])
    msg.attach_alternative(html_content, "text/html")

    # Send the email
    msg.send()

    TransferEmailLog.objects.create(
        user=user,
        subject=subject,
        body=text_content,
    )


def send_transfer_credit_alert(to_account, from_account, amount, transfer_date, transfer_time, transfer_id, description):
    user =to_account.user
    subject = f"SSBeNS Credit Alert: N{humanize.intcomma(amount)} credited to your account"

    # Render the HTML content using a template
    html_content = render_to_string('bank/credit_alert_by_others.html', {
        'user': to_account,
        'sender': from_account,
        'amount': amount,
        'description': description,
        'transfer_time': transfer_time,
        'transfer_date': transfer_date,
        'transfer_id': transfer_id
    })

    # Create a plain text version of the email
    text_content = render_to_string('bank/credit_alert_by_others.txt', {
    'user': to_account,
    'amount': amount,
    'transfer_date': transfer_date,
    'transfer_time': transfer_time,
    'sender': from_account,
    'transfer_id': transfer_id,
    'description': description,
    })

    # Create the email message object and attach the HTML content as an alternative
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_account.user.email])
    msg.attach_alternative(html_content, "text/html")

    # Send the email
    msg.send()

    TransferEmailLog.objects.create(
        user=user,
        subject=subject,
        body=text_content,
    )



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
        form = Current_Account_Form()
    return render(request, 'bank/current_account.html', {'form': form})



# #this is used to authenticate this view, a login decorator should be used later on
@login_required
def profile(request): 

    user_request = request.user
    #to get the users details
    current_user_id = request.user.id
    user = ExtendedUser.objects.get(id=current_user_id)
    return render(request, 'bank/profile.html',{'user':user})



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


@login_required
def credit(request):
    user = request.user
    current_accounts = CreateCurrentAccount.objects.filter(user=user)
    savings_accounts = CreateSavingsAccount.objects.filter(user=user)
    context = {
        'current_accounts': current_accounts,
        'savings_accounts': savings_accounts,
    }
    
    if request.method == 'POST':
        dest_account = request.POST.get('dest_account')
        amount = request.POST.get('amount')
        credit_source = request.POST.get('credit_source')
        description = request.POST.get('description')
        pin = request.POST.get('pin')
            # Verify user's PIN
        if not user.check_pin(pin):
            messages.error(request, "Invalid PIN.")
            return redirect('credit')

        # Retrieve the destination user by account number
        try:
            dest_account = CreateCurrentAccount.objects.get(account_number=dest_account)
        except CreateCurrentAccount.DoesNotExist:
            try:
                dest_account = CreateSavingsAccount.objects.get(account_number=dest_account)
            except CreateSavingsAccount.DoesNotExist: 
                messages.error(request, "Destination account does not exist.")
                return redirect('credit')

        amount = decimal.Decimal(amount)

        with transaction.atomic():
            
            # Create a new Credit object and save it
            credit = Credit(dest_account=dest_account.user, dest_account_number=dest_account.account_number, credit_amount=amount, credit_source=credit_source, credit_description=description)
            credit.save()

            # Update the account balance for the user
            dest_account.account_balance += amount
            dest_account.save()

            credit_date = credit.credit_time.date()
            credit_time = credit.credit_time.time()
            credit_id = credit.credit_id

            # Send a credit alert email to the user
            send_credit_alert(dest_account, amount, credit_source, credit_date, credit_time, credit_id, description)

            messages.success(request, "Credit made successfully!")
            return redirect('credit')

    return render(request, 'bank/credit.html', context)



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
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        pin = request.POST.get('pin')

        # Verify user's PIN
        if not user.check_pin(pin):
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
            transfer = Transfer(from_user=from_account.user, from_account_number=from_account.account_number, to_user=to_account.user, to_account_number=to_account.account_number, transfer_amount=amount, transfer_description=description)
            transfer.save()

            # Update the account balances for the sender and recipient
            from_account.account_balance -= amount
            to_account.account_balance += amount
            from_account.save()
            to_account.save()

            transfer_date = transfer.transfer_date.date()
            transfer_time = transfer.transfer_date.time()
            transfer_id = transfer.transfer_id            

            send_transfer_debit_alert(from_account, to_account, amount, transfer_date, transfer_time, transfer_id,description)
            send_transfer_credit_alert(to_account, from_account, amount, transfer_date, transfer_time, transfer_id, description)

            messages.success(request, "Transfer made successfully!")
            return redirect('transfer')

    return render(request, 'bank/transfer.html', context)


@login_required
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
            # make this view do something else instead of returning an html page dthat doesnt exist 
    return render(request, 'bank/search_account.html') 
  

@login_required
def transaction_history(request):
    user = request.user
    transactions = Transfer.objects.filter(from_user=user).order_by('-transfer_date')
    paginator = Paginator(transactions, 4)  # Show 10 transactions per page
    page = request.GET.get('page')
    transactions_list = paginator.get_page(page)
    context = {
        'transactions' : transactions,
        'transactions_list' : transactions_list
    }

    return render(request, 'bank/transaction_history.html', context)



















