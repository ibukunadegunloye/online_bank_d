from django.shortcuts import render, redirect, HttpResponse
from .forms import LoginForm , ExtendedUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import ExtendedUser, AccountVerificationEmailLog, WelcomeEmailLog
from bank.models import CreateCurrentAccount, CreateSavingsAccount
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .utils import generate_token
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import threading

# Create your views here.

class EmailThread(threading.Thread):

    def __init__(self,msg):
        self.msg = msg
        threading.Thread.__init__(self)

    def run(self):
        self.msg.send()


def send_activation_email(user, request):
    current_site = get_current_site(request).domain
    subject = 'Activate your account'

    context = {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user),
    }
    # Render the HTML content using a template
    html_content = render_to_string('account/activate.html', context)

    # Create a plain text version of the email
    text_content = render_to_string('account/activate.txt', context)

    # Create the email message object and attach the HTML content as an alternative
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
    msg.attach_alternative(html_content, "text/html")

    # Send the email
    EmailThread(msg).start()
    
    AccountVerificationEmailLog.objects.create(
        user=user,
        email_subject=subject,
        email_body=text_content,
    )


def welcome_mail(user):
    subject = 'Welcome to Sorosoke Bank'
    account_user = CreateSavingsAccount.objects.get(user=user)

    html_content = render_to_string('account/welcome_mail.html', {
        'user': user, 'account_user':account_user,
    })

    # Create a plain text version of the email
    text_content = render_to_string('account/welcome_mail.txt', {
        'user': user, 'account_user':account_user,
    })

    # Create the email message object and attach the HTML content as an alternative
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
    msg.attach_alternative(html_content, "text/html")

    # Send the email
    EmailThread(msg).start() 

    WelcomeEmailLog.objects.create(
        user=user,
        email_subject=subject,
        email_body=text_content,
    )






def login_account(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            
            #check if the user is email verified
            if user.is_email_verified == False:
                messages.error(request, 'Please chceck your mailbox to activate your account')
                return render (request, 'account/login.html', {'form':form})

            if user is not None:
                login(request, user)
                messages.success(request, f'You have logged in successfully {user.first_name}!')
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


@csrf_protect
def register_account(request):
    if request.method == 'POST':
        form = ExtendedUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            savings_account = CreateSavingsAccount(user=user)
            savings_account.save()

            send_activation_email(user, request)
            messages.success(request, f'An email has been sent to activate your account!')

            return redirect('login')
    else:
        form = ExtendedUserForm()
    return render(request, 'account/register_account.html', {'form': form})


def activate_user(request, uidb64, token):
    print(request)
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = ExtendedUser.objects.get(pk=uid)
        print(user.first_name)
    except Exception as e:
        user = None

    if user is not None and generate_token.check_token(user, token):
        try:
            user.is_email_verified = True
            user.save()
            welcome_mail(user)
            return redirect('login')
        except Exception as e:
           print('bingo')         
    else:
        return render(request, 'account/activation_failed.html', {'user': user})




