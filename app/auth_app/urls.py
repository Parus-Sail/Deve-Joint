from django.urls import path

from . import views
from .apps import AuthAppConfig

app_name = AuthAppConfig.name
urlpatterns = [
    path("login/", views.LoginUser.as_view(), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.RegisterUser.as_view(), name="register"),
    path("password-reset/", views.UserPasswordReset.as_view(), name="password_reset"),
    path("password-reset/done/", views.UserPasswordResetDone.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.UserPasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.UserPasswordResetComplete.as_view(), name="password_reset_complete"),
    path("confirm-email/", views.ShowConfirmationEmail.as_view(), name="confirm_email"),
    path("verify-email/<uidb64>/<token>/", views.VerifyEmail.as_view(), name="verify_email"),
    path("failed-verify-email/", views.FailedVerifyEmail.as_view(), name="failed_verify_email"),
    path("profile/", views.UserUpdateView.as_view(), name="profile"),
]
