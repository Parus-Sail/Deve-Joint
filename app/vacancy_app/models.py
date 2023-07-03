from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class PaymentAccount(models.Model):

    class Status(models.TextChoices):
        APP = "APP", _("Approved")
        NOT_APP = "NOT_APP", _("Not Approved")
        REQ_APP = "REQ_APP", _("Request Approve")
        BLOCKED = "BLC", _("Blocked")

    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))
    address = models.CharField(null=True, blank=True, max_length=255, verbose_name=_("address"))
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.NOT_APP, verbose_name=_("status"))
    type = models.CharField(max_length=255, verbose_name=_("type"))
    director_name = models.CharField(null=True, blank=True, max_length=255, verbose_name=_("director name"))
    bank = models.CharField(null=True, blank=True, max_length=255, verbose_name=_("bank"))
    tax_number = models.CharField(null=True, blank=True, max_length=255, verbose_name=_("tax identification number"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created time"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("update_time"))
    email = models.EmailField(verbose_name=_("email address"))

    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        verbose_name=_("owner"),
        related_name=_("payment_account"),
    )

    def get_absolute_url(self):
        return reverse("vacancy:payment_account_detail", kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("Payment Account")
        verbose_name_plural = _("Payment Account's")
        ordering = ["-update_at", "name"]

    def __str__(self):
        return f"{self.name}, {self.description[:20]}, {self.get_status_display()}"


class Company(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACT", _("Active")
        NOT_ACTIVE = "NOT_ACT", _("Not Active")

    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))
    location = models.CharField(max_length=255, verbose_name=_("location"))
    url = models.URLField(null=True, blank=True, verbose_name=_("web address"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created time"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("update_time"))
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.NOT_ACTIVE,
                              verbose_name=_("status"))

    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        verbose_name=_("owner"),
        related_name=_("company"),
    )
    payment_account = models.ForeignKey(
        PaymentAccount,
        on_delete=models.PROTECT,
        verbose_name=_("payment account"),
        related_name=_("company_list"),
    )

    def get_absolute_url(self):
        return reverse("vacancy:company_detail", kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Company's")
        ordering = ["-update_at", "name"]

    def __str__(self):
        return f"{self.name}, {self.description[:20]}, {self.get_status_display()}"
