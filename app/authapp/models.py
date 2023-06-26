from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class BaseOpenSailUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["username"]

    def get_current_name(self):
        """
        Функция возвращает полное имя пользователя, а если его нет: username
        """
        if self.get_full_name():
            return self.get_full_name()
        return self.username

    def __str__(self):
        return self.get_current_name()

    @staticmethod
    def get_absolute_url():
        return reverse("authapp:profile")
