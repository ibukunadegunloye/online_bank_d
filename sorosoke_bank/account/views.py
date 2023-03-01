from django.shortcuts import render, redirect
from .forms import LoginForm , ExtendedUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import ExtendedUser
from bank.models import CreateCurrentAccount, CreateSavingsAccount


# Create your views here.



from django.contrib.auth import authenticate, login, logout

def login_account(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'You have logged in successfully {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid form input')
    else:
        form = LoginForm()
    return render (request, 'account/login.html', {'form':form})


def logout_account(request):
    logout(request)
    messages.success(request, f'You have logged out successfully!')
    return redirect('login')


def register_account(request):
    if request.method == 'POST':
        form = ExtendedUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            savings_account = CreateSavingsAccount(user=user)
            savings_account.save()
            return redirect('login')
    else:
        form = ExtendedUserForm()
    return render(request, 'account/register_account.html', {'form': form})


