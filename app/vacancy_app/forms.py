from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from vacancy_app.models import Company, PaymentAccount

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

        fields = ("name", "description", "location", "url", "status", "payment_account")
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
