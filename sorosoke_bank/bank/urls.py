from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('savings_account/', views.savings_account, name='savings_account'),
        path('current_account/', views.current_account, name='current_account'),
]
