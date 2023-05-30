from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'accounts'

urlpatterns = [
    path('create/', views.AccountCreateView.as_view(), name='accounts_create'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('logout/', views.LogoutPage.as_view(), name='logout'),
]