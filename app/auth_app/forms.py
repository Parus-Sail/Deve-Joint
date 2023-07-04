from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError

from .utils import DivErrorList, SendEmailForVerify

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ("email", "username", "password1", "password2")
        for field in fields:
            # кастомный css для полей
            self.fields[field].widget.attrs.update({"class": "form-control"})
            # убираем стандартную помощь от Django
            self.fields[field].help_text = None
        # кастомный css для ошибок
        self.error_class = DivErrorList

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) < 4:
            raise ValidationError("Длина имени минимум 4 символа!")

        return username


class CustomUserChangeForm(UserChangeForm):
    avatar = forms.ImageField(widget=forms.FileInput())
    password = None
    email = forms.CharField(disabled=True)
    username = forms.CharField(disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ("first_name", "last_name", "email", "username", 'age', 'country', 'city', 'about', 'avatar')
        for field in fields:
            # кастомный css для полей
            self.fields[field].widget.attrs.update({"class": "form-control"})
        self.fields['avatar'].widget.attrs['class'] = 'custom-file-input'
        # кастомный css для ошибок
        self.error_class = DivErrorList

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", 'age', 'country', 'city', 'about', 'avatar')


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
                    "Email not verified, please verify your email.",
                    code="invalid_login",
                )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class CustomUserPasswordConfirmForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ("new_password1", "new_password2")
        for field in fields:
            # кастомный css для полей
            self.fields[field].widget.attrs.update({"class": "form-control"})
            # убираем стандартную помощь от Django
            self.fields[field].help_text = None
        # кастомный css для ошибок
        self.error_class = DivErrorList
