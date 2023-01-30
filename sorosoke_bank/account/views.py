from django.shortcuts import render, redirect
from .forms import RegisterAccountForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.


def register_account(request):
    if request.method == 'POST':
        form = RegisterAccountForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'{username} your account has been created successfully!, You may now login.')
            return redirect ('login')
    else:
        form = RegisterAccountForm()
    return render (request, 'account/register_account.html', {'form':form})


# def login_account(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, f'You have logged in successfully {username}!')
#             return redirect('home')
#     else:
#         form = LoginForm()
#     return render (request, 'authenticate/login.html', {'form':form})

# def logout_account(request):
#     logout(request)
#     messages.success(request, f'You have logged out successfully!')
#     return redirect('login_account')