from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .forms import StoreUserCreationForm, StoreUserChangeForm
from .models import User


class UserAdmin(UserAdmin):
    add_form = StoreUserCreationForm
    form = StoreUserChangeForm
    model = User
    list_display = ['email', 'username', ]


admin.site.register(User, UserAdmin)
