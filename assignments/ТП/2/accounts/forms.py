from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class StoreUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'user_type')


class StoreUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'user_type')
