from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Company, PaymentAccount, Vacancy
from .utils import DivErrorList


class PaymentAccountCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ("name", "description", "type", "director_name", "bank", "tax_number", 'email', 'address')
        for field in fields:
            # кастомный css для полей
            self.fields[field].widget.attrs.update({"class": "form-control"})
        # кастомный css для ошибок
        self.error_class = DivErrorList

    class Meta:
        model = PaymentAccount
        exclude = ("status", "owner")


class PaymentAccountModerationCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = (
            "name",
            "description",
            "type",
            "director_name",
            "bank",
            "tax_number",
            "status",
            "email",
            "address",
        )
        for field in fields:
            # кастомный css для полей
            # поля нельзя редактировать
            self.fields[field].widget.attrs.update({"class": "form-control"})
            self.fields[field].widget.attrs.update({"readonly": "True"})
        # кастомный css для ошибок
        self.error_class = DivErrorList

    class Meta:
        model = PaymentAccount
        exclude = ('owner',)


class CompanyCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # получаем request в форме
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        fields = ("name", "description", "location", "url", "status", "payment_account", "avatar")
        for field in fields:
            # кастомный css для полей
            self.fields[field].widget.attrs.update({"class": "form-control"})
        # кастомный css для ошибок
        self.error_class = DivErrorList
        # только подтвержденный payment account и правильный user
        self.fields['payment_account'].queryset = self.fields['payment_account'].queryset.filter(
            status=PaymentAccount.Status.APP, owner=self.request.user)
        self.fields["payment_account"].empty_label = _("Choose payment account")

    def clean(self):
        super().clean()
        if self.cleaned_data['payment_account'].status != PaymentAccount.Status.APP:
            raise ValidationError(_("Wrong payment account status"))

    class Meta:
        model = Company
        exclude = ("owner",)


class VacancyCreationForm(forms.ModelForm):
    # Пользователю запрещена блокировка
    USER_ALLOWED_STATUS = (
        ("ACT", _("Active")),
        ("NOT_ACT", _("Not Active")),
    )
    status = forms.CharField(widget=forms.Select(choices=USER_ALLOWED_STATUS))

    def __init__(self, *args, **kwargs):
        # получаем request в форме
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        fields = (
            "name",
            "description",
            "location",
            "salary_from",
            "salary_to",
            "requirements",
            "status",
            "company",
            "applicant_level",
            "employment_type",
            "job_type",
        )
        for field in fields:
            # кастомный css для полей
            self.fields[field].widget.attrs.update({"class": "form-control"})
        # кастомный css для ошибок
        self.error_class = DivErrorList
        # только активная компания и правильный user
        self.fields['company'].queryset = self.fields['company'].queryset.filter(status=Company.Status.ACTIVE,
                                                                                 owner=self.request.user)
        self.fields["company"].empty_label = _("Choose company")

    def clean(self):
        super().clean()
        if self.cleaned_data['company'].status != Company.Status.ACTIVE:
            raise ValidationError(_("Wrong company status"))

        # Зарплата "от" должна быть меньше зарплаты "до", если указано
        if self.cleaned_data['salary_from'] and self.cleaned_data['salary_to']:
            if self.cleaned_data['salary_from'] > self.cleaned_data['salary_to']:
                self.cleaned_data['salary_from'], self.cleaned_data['salary_to'] = self.cleaned_data[
                    'salary_to'], self.cleaned_data['salary_from']

    class Meta:
        model = Vacancy
        exclude = ("owner", "reason_for_block")


class VacancyModerationCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # получаем request в форме
        # self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        fields = (
            "name",
            "description",
            "location",
            "salary_from",
            "salary_to",
            "requirements",
            "company",
            "applicant_level",
            "employment_type",
            "job_type",
            "status",
        )
        for field in fields:
            # кастомный css для полей
            self.fields[field].widget.attrs.update({"class": "form-control"})
            # поля нельзя редактировать кроме status и reason_for_block
            self.fields[field].widget.attrs.update({"readonly": "True"})
        self.fields["company"].disabled = True
        self.fields["applicant_level"].disabled = True
        self.fields["employment_type"].disabled = True
        self.fields["job_type"].disabled = True
        self.fields["reason_for_block"].widget.attrs.update({"class": "form-control"})
        # кастомный css для ошибок
        self.error_class = DivErrorList

    def clean_reason_for_block(self):
        reason_for_block = self.cleaned_data["reason_for_block"]
        status = self.cleaned_data['status']
        if status == Vacancy.Status.BLOCKED:
            if not self.cleaned_data['reason_for_block']:
                raise ValidationError(_("Need reason for block!"))
        return reason_for_block

    class Meta:
        model = Vacancy
        exclude = ("owner",)
