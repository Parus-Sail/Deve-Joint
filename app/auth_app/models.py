from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class BaseOpenSailUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    email_verify = models.BooleanField(default=False)
    age = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('age'))
    avatar = models.ImageField(upload_to='user_avatar', blank=True, verbose_name=_('photo'))
    about = models.TextField(blank=True, null=True, verbose_name=_('about yourself'))
    country = models.CharField(max_length=50, verbose_name=_('country'), blank=True, null=True)
    city = models.CharField(max_length=50, verbose_name=_('city'), blank=True, null=True)
    phone = models.CharField(max_length=150, null=True, verbose_name=_('Phone'))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
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
        return reverse("auth_app:profile")
