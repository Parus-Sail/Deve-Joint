from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError

from .utils import SendEmailForVerify

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) < 4:
            raise ValidationError("Длина имени минимуму 4 символа!")

        return username


class CustomUserChangeForm(UserChangeForm):
    password = None
    email = forms.CharField(disabled=True)
    username = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")


class CustomUserLoginForm(AuthenticationForm, SendEmailForVerify):

    class Meta:
        model = User

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)

            if self.user_cache is not None and not self.user_cache.email_verify:
                self.send_email_for_verify(user=self.user_cache)
                raise ValidationError(
                    "Email не подтвержден, проверьте свой почтовый ящик",
                    code="invalid_login",
                )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
