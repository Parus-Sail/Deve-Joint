from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet
from vacancy_app.models import PaymentAccount


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
