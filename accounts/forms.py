from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'bio', 'profile', 'last_name', 'first_name', 'email')

class LoginForm(AuthenticationForm):
    pass