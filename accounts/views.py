from django.views import generic
from .models import CustomUser
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import MyUserCreationForm, LoginForm


class AccountCreateView(generic.CreateView):
    Model = CustomUser
    form_class = MyUserCreationForm
    template_name = 'accounts/accounts_create.html'
    success_url = reverse_lazy('insta:top')

class LoginPage(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('insta:top')

class LogoutPage(LogoutView):
    template_name = 'accounts/logout.html'
    success_url = reverse_lazy('insta:top')