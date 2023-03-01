from django.urls import path
from . import views

urlpatterns = [
    path('register_account', views.register_account, name='register_account'),
    path('login', views.login_account, name='login'),
    path('logout', views.logout_account, name='logout')
]
