from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.contrib.auth.hashers import make_password, check_password
from .utils import validate_min_length
import uuid



# Create your models here.



class ExtendedBaseManager(UserManager):

    def _create_user(self, email, first_name, last_name, password, phone_number, address, gender, occupation, marital_status, date_of_birth, nationality, pin, **extra_fields):
        if not email:
            raise ValueError('You have provided an invalid email.')
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, phone_number=phone_number, address=address, gender=gender, occupation=occupation, marital_status=marital_status, date_of_birth=date_of_birth, nationality=nationality, **extra_fields)
        user.set_password(password)
        user.pin = make_password(pin)  # hash the pin and set it
        user.save(using=self._db)

        return user   

    def create_user(self, email, password, first_name, last_name, phone_number, address, gender, occupation, marital_status, date_of_birth, nationality, pin, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active',True)
        return self._create_user(email, first_name, last_name, password, phone_number, address, gender, occupation, marital_status, date_of_birth, nationality, pin, **extra_fields)

    def create_superuser(self, email, password, first_name=None, last_name=None, phone_number=None, address=None, gender=None, occupation=None, marital_status=None, date_of_birth=None, nationality=None, pin=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, first_name, last_name, password, phone_number, address, gender, occupation, marital_status, date_of_birth, nationality, pin, **extra_fields)



class ExtendedUser(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    ]

    ACCOUNT_TYPE_CHOICES = [
        ('Savings_Account','Savings Account')
    ]

    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255)
    pin = models.CharField(max_length=6)
    phone_number = PhoneNumberField(blank=False, null=True, unique=True)
    address = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    occupation = models.CharField(max_length=255, null=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, null=True)
    date_of_birth = models.DateField(null=True)
    nationality = CountryField(blank_label='(select Nationality)', null=True, blank=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = ExtendedBaseManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def set_pin(self, raw_pin):
        self.pin = make_password(raw_pin)

    def check_pin(self, raw_pin):
        return check_password(raw_pin, self.pin)

    def save(self, *args, **kwargs):
        self.password = self.password
        self.pin = make_password(self.pin)
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"First-Name: {self.first_name} || Last-Name:{self.last_name} || Email: {self.email} || Gender: {self.gender} || Account Type: {self.account_type} || Nationality: {self.nationality}"



class AccountVerificationEmailLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, null=True, related_name='account_verification_email_log')
    email_subject = models.CharField(max_length=100)
    email_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Activation Email Log for {self.user.first_name} {self.user.last_name}"


class WelcomeEmailLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, null=True, related_name='welcome_email_log')
    email_subject = models.CharField(max_length=100)
    email_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Welcome Email Log for {self.user.first_name} {self.user.last_name}"
    
