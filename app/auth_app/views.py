from auth_app import forms as auth_app_forms
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.views import (
    LoginView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView

from .utils import SendEmailForVerify

User = get_user_model()


class RegisterUser(SendEmailForVerify, CreateView):
    form_class = auth_app_forms.CustomUserCreationForm
    template_name = "auth_app/registration/registration.html"
    success_url = reverse_lazy("auth_app:login")

    def form_valid(self, form):
        user = form.save()
        try:
            self.send_email_for_verify(user=user)
        except Exception:
            pass
        return redirect("auth_app:confirm_email")


class LoginUser(LoginView):
    form_class = auth_app_forms.CustomUserLoginForm
    template_name = "auth_app/registration/login.html"

    def get_success_url(self):
        return reverse_lazy("main:index")


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = auth_app_forms.CustomUserChangeForm
    template_name = "auth_app/registration/profile.html"
    success_url = reverse_lazy("main:index")

    def get_object(self):
        return self.request.user


class UserPasswordReset(PasswordResetView):
    template_name = "auth_app/registration/password_reset.html"
    email_template_name = "auth_app/registration/password_reset_email.html"
    success_url = reverse_lazy("auth_app:password_reset_done")


class UserPasswordResetDone(PasswordResetDoneView):
    template_name = "auth_app/registration/password_reset_done.html"


class UserPasswordResetConfirm(PasswordResetConfirmView):
    form_class = auth_app_forms.CustomUserPasswordConfirmForm
    template_name = "auth_app/registration/password_reset_confirm.html"
    success_url = reverse_lazy("auth_app:password_reset_complete")


class UserPasswordResetComplete(PasswordResetCompleteView):
    template_name = "auth_app/registration/password_reset_complete.html"


class ShowConfirmationEmail(TemplateView):
    template_name = "auth_app/registration/confirmation_email.html"


class VerifyEmail(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect("main:index")
        else:
            return redirect("auth_app:failed_verify_email")

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user


class FailedVerifyEmail(TemplateView):
    template_name = "auth_app/registration/failed_verify_email.html"


def logout_user(request):
    logout(request)
    return redirect("auth_app:login")
