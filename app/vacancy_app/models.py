from pathlib import Path
from time import time

from config.settings import STATIC_ROOT
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def company_avatars_path(instance, filename):
    """
    file will be uploaded to
    MEDIA_ROOT / company name / avatars / <filename>
    """
    num = int(time() * 1000)
    suffix = Path(filename).suffix
    return f"company_{instance.name}/avatars/pic_{num}{suffix}"


class PaymentAccount(models.Model):

    class Status(models.TextChoices):
        APP = "APP", _("Approved")
        NOT_APP = "NOT_APP", _("Not Approved")
        REQ_APP = "REQ_APP", _("Request Approve")
        BLOCKED = "BLC", _("Blocked")

    name = models.CharField(max_length=255, verbose_name=_("name"), unique=True)
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

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = PaymentAccount.objects.get(pk=self.pk)
            # не был заблокирован, стал заблокирован
            if orig.status != self.Status.BLOCKED and self.Status.BLOCKED:
                # если аккаунт был подтвержден, а потом был заблокирован, то все компании делаем неактивными
                for company_obj in self.company_list.all():
                    company_obj.status = Company.Status.NOT_ACTIVE
                    company_obj.save()
        super(PaymentAccount, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Payment Account")
        verbose_name_plural = _("Payment Account's")
        ordering = ["-update_at", "name"]

    def __str__(self):
        return f"{self.name}, {self.get_status_display()}"


class Company(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACT", _("Active")
        NOT_ACTIVE = "NOT_ACT", _("Not Active")

    name = models.CharField(max_length=255, verbose_name=_("name"), unique=True)
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
    avatar = models.ImageField(upload_to=company_avatars_path, verbose_name=_("avatar"), null=True, blank=True)

    def get_absolute_url(self):
        return reverse("vacancy:company_detail", kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Company.objects.get(pk=self.pk)
            # если старое состояние было активно, а новое неактивно,
            # то изменяем в новое состояние неактивно все вакансии
            if orig.status == self.Status.ACTIVE and self.status != self.Status.ACTIVE:
                # если компания стала неактивным делаем неактивными все ее вакансии, если они были активны
                for vacancy_obj in self.vacancy_list.all():
                    if vacancy_obj.status == Vacancy.Status.ACTIVE:
                        vacancy_obj.status = self.Status.NOT_ACTIVE
                    vacancy_obj.save()

        super(Company, self).save(*args, **kwargs)

    # def get_avatar(self):
    #     if self.avatar:
    #         return self.avatar.url
    #     return STATIC_ROOT

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("name"), name=_("company name case insensitive")),
        ]
        verbose_name = _("Company")
        verbose_name_plural = _("Company's")
        ordering = ["-update_at", "name"]

    def __str__(self):
        return f"{self.name}, {self.get_status_display()}"


class ApplicantLevel(models.Model):
    """
    Trainee, Junior, Middle, Senior
    """

    name = models.CharField(max_length=255, unique=True, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))
    sort_order = models.PositiveIntegerField(verbose_name=_("sort order"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created time"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("update_time"))

    # def get_absolute_url(self):
    #     return reverse("vacancy:company_detail", kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("Applicant Level")
        verbose_name_plural = _("Applicant Level's")
        ordering = [
            "sort_order",
        ]

    def __str__(self):
        return self.name


class EmploymentType(models.Model):
    """
    EmploymentType:
    Remote, Full Time, Contract, Part Time, Freelance
    """

    name = models.CharField(max_length=255, unique=True, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))
    sort_order = models.PositiveIntegerField(verbose_name=_("sort order"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created time"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("update_time"))

    # def get_absolute_url(self):
    #     return reverse("vacancy:company_detail", kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("Employment Type")
        verbose_name_plural = _("Employment Type's")
        ordering = [
            "sort_order",
        ]

    def __str__(self):
        return self.name


class JobType(models.Model):
    """
    Job types:
    Web design, Marketing, Customer Support, Engineer, Devops, Programming
    """

    name = models.CharField(max_length=255, unique=True, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))
    sort_order = models.PositiveIntegerField(verbose_name=_("sort order"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created time"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("update_time"))

    class Meta:
        verbose_name = _("Job Type")
        verbose_name_plural = _("Job Type's")
        ordering = [
            "sort_order",
        ]

    def __str__(self):
        return self.name


class Vacancy(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACT", _("Active")
        NOT_ACTIVE = "NOT_ACT", _("Not Active")
        BLOCKED = "BLK", _("Blocked")

    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))
    requirements = models.TextField(null=True, blank=True, verbose_name=_("requirements"))
    location = models.CharField(max_length=255, verbose_name=_("location"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created time"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("update_time"))
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.NOT_ACTIVE,
                              verbose_name=_("status"))
    salary_from = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("salary from"))
    salary_to = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("salary to"))
    reason_for_block = models.TextField(null=True, blank=True, verbose_name=_("reason for block"))
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        verbose_name=_("owner"),
        related_name=_("vacancy"),
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        verbose_name=_("company"),
        related_name=_("vacancy_list"),
    )

    # Trainee, Junior, Middle, Senior
    applicant_level = models.ManyToManyField(
        ApplicantLevel,
        verbose_name=_("Applicant Level"),
        blank=True,
        related_name="level_vacancy_list",
    )

    #  Remote, Full Time, Contract, Part Time, Freelance
    employment_type = models.ManyToManyField(
        EmploymentType,
        verbose_name=_("Employment Type"),
        blank=True,
        related_name="employment_type_vacancy_list",
    )

    # Web Design, Marketing, Customer Support, Engineer, Devops, Programming, Testing
    job_type = models.ManyToManyField(
        JobType,
        verbose_name=_("Job Type"),
        blank=True,
        related_name="job_type_vacancy_list",
    )

    def get_absolute_url(self):
        return reverse("vacancy:vacancy_detail", kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("Vacancy")
        verbose_name_plural = _("Vacancy's")
        ordering = ["-update_at", "name"]

    def __str__(self):
        return f"{self.name}, {self.get_status_display()}"
