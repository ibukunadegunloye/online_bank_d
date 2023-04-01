from django.urls import path
from . import views

urlpatterns = [
    path('register/account', views.register_account, name='register_account'),
    path('login', views.login_account, name='login'),
    path('logout', views.logout_account, name='logout'),
    path('activate_user/<uidb64>/<token>/', views.activate_user, name='activate_user'),
]
