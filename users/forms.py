from django.contrib.auth import forms as auth_forms
from django import forms
from users.models import User


class UserRegisterForm(auth_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ('email','first_name', 'last_name', 'phone', 'country', 'avatar', 'password1', 'password2')


class UserProfileForm(auth_forms.UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'country', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
