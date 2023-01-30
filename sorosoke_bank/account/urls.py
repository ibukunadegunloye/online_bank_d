from django.urls import path
from . import views

urlpatterns = [
    path('register_account', views.register_account, name='register_account'),
]
