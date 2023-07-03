from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from django_filters.views import FilterView
from vacancy_app import forms as vacancy_forms
from vacancy_app import models as vacancy_models

from .filters import PaymentAccountFilter
from .mixins import RequestFormKwargsMixin, StaffRequiredMixin


class JobsListingView(TemplateView):
    template_name: str = "vacancy_app/job_listing.html"


class JobsDetailView(TemplateView):
    template_name: str = "vacancy_app/job_details.html"


# ======Payment Account views start here=========
class PaymentAccountCreateView(LoginRequiredMixin, CreateView):
    form_class = vacancy_forms.PaymentAccountCreationForm
    template_name = 'vacancy_app/payment_account_form.html'
    success_url = reverse_lazy("vacancy_app:payment_account_list")

    # владелец компании текущий пользователь
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PaymentAccountDetailView(LoginRequiredMixin, DetailView):
    template_name = 'vacancy_app/payment_account_detail.html'
    model = vacancy_models.PaymentAccount


class PaymentAccountListView(LoginRequiredMixin, ListView):
    template_name = 'vacancy_app/payment_account_list.html'
    model = vacancy_models.PaymentAccount

    def get_queryset(self):
        queryset = vacancy_models.PaymentAccount.objects.filter(owner=self.request.user)
        return queryset


class PaymentAccountUpdateView(LoginRequiredMixin, UpdateView):
    form_class = vacancy_forms.PaymentAccountCreationForm
    model = vacancy_models.PaymentAccount
    template_name = 'vacancy_app/payment_account_form.html'
    success_url = reverse_lazy("vacancy:payment_account_list")

    # Редактирует только владелец и только в статусе не подтверждено
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user or obj.status != vacancy_models.PaymentAccount.Status.NOT_APP:
            raise PermissionDenied()
        return obj


class PaymentAccountDeleteView(LoginRequiredMixin, DeleteView):
    model = vacancy_models.PaymentAccount
    template_name = 'vacancy_app/payment_account_confirm_delete.html'
    success_url = reverse_lazy("vacancy:payment_account_list")

    # Удаляет только владелец и только в статусе не подтверждено
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user or obj.status != vacancy_models.PaymentAccount.Status.NOT_APP:
            raise PermissionDenied()
        return obj


# ======Payment Account moderation views start here=========
class PaymentAccountChangeStatus(LoginRequiredMixin, View):

    def get(self, request, pk, status):
        payment_account = vacancy_models.PaymentAccount.objects.get(pk=pk)
        # статус меняет пользователь или модератор
        if payment_account.owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied()
        # пользователь может изменить только один статус
        if payment_account.owner == self.request.user and status != vacancy_models.PaymentAccount.Status.REQ_APP:
            raise PermissionDenied()
        payment_account.status = status
        payment_account.save()
        return redirect("vacancy:payment_account_list")


class SearchResultPaymentAccountModerationListView(LoginRequiredMixin, StaffRequiredMixin, FilterView):
    model = vacancy_models.PaymentAccount
    template_name = 'vacancy_app/payment_account_moderation_search_results.html'
    filterset_class = PaymentAccountFilter
    context_object_name = 'object_list'


class PaymentAccountModerationUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    form_class = vacancy_forms.PaymentAccountModerationCreationForm
    model = vacancy_models.PaymentAccount
    template_name = 'vacancy_app/payment_account_moderation_form.html'
    success_url = reverse_lazy("vacancy:payment_account_moderation_list")


class UserProfileView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    """
    Детали профайла пользователя для модерации, желательно вывести все поля, доступно только для is_staff
    """
    model = get_user_model()
    template_name = "vacancy_app/user_profile_detail.html"


# ===============Company views start here=====================
class CompanyCreateView(LoginRequiredMixin, RequestFormKwargsMixin, CreateView):
    form_class = vacancy_forms.CompanyCreationForm
    template_name = 'vacancy_app/company_form.html'
    success_url = reverse_lazy("vacancy_app:company_list")

    # владелец компании текущий пользователь
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = vacancy_models.Company


class CompanyListView(LoginRequiredMixin, ListView):
    model = vacancy_models.Company

    def get_queryset(self):
        queryset = vacancy_models.Company.objects.filter(owner=self.request.user)
        return queryset


class CompanyUpdateView(LoginRequiredMixin, RequestFormKwargsMixin, UpdateView):
    form_class = vacancy_forms.CompanyCreationForm
    model = vacancy_models.Company
    template_name = 'vacancy_app/company_form.html'
    success_url = reverse_lazy("vacancy:company_list")

    # Редактирует только владелец
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied()
        return obj


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = vacancy_models.Company
    success_url = reverse_lazy("vacancy:company_list")

    # Удаляет только владелец
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied()
        return obj
