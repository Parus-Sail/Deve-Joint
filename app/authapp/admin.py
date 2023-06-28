from authapp import forms as authapp_forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = authapp_forms.CustomUserCreationForm
    form = authapp_forms.CustomUserChangeForm
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
