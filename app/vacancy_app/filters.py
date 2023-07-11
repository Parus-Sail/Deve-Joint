from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, filters

from .models import PaymentAccount, Vacancy


class PaymentAccountFilter(FilterSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # custom css
        self.filters['status'].field.widget.attrs.update({"class": "form-control"})
        self.filters["status"].field.empty_label = _("Select status")
        self.filters["status"].field.label = ''

    class Meta:
        model = PaymentAccount
        fields = [
            'status',
        ]


class VacancyFilter(FilterSet):
    owner = filters.ModelChoiceFilter(queryset=get_user_model().objects.filter(
        is_superuser=False, is_staff=False, is_active=True).order_by('username'))
    description = filters.CharFilter(lookup_expr='icontains', label='Description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # custom css
        self.filters['status'].field.widget.attrs.update({"class": "form-control"})
        self.filters["status"].field.empty_label = _("Select status")
        self.filters["status"].field.label = None

        self.filters['owner'].field.widget.attrs.update({"class": "form-control"})
        self.filters["owner"].field.empty_label = _("Select owner")
        self.filters["owner"].field.label = None

        self.filters['description'].field.widget.attrs.update({"class": "form-control"})
        self.filters["description"].field.empty_label = _("Description")
        self.filters["description"].field.label = None

    class Meta:
        model = Vacancy
        fields = ['owner', 'status', 'description']
