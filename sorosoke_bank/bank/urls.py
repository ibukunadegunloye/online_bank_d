from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('savings/', views.savings, name='savings'),
    path('current/', views.current, name='current'),
    path('credit/', views.credit, name='credit'),
    path('transfer/', views.transfer, name='transfer'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),
    path('savings_account/', views.savings_account, name='savings_account'),
    path('current_account/', views.current_account, name='current_account'),
    path('search/account', views.search_account, name='search_account'),
]
