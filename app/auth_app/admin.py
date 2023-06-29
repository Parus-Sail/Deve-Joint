from auth_app import forms as auth_app_forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = auth_app_forms.CustomUserCreationForm
    form = auth_app_forms.CustomUserChangeForm
    model = User
    list_display = ["email", "username"]
    list_display_links = ("username", "email")

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            "Дополнительные обязательные поля",
            {
                "fields": ("email",)
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
