from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django_filters.views import FilterView

from . import forms as vacancy_forms
from . import models as vacancy_models
from .filters import PaymentAccountFilter, VacancyFilter
from .mixins import RequestFormKwargsMixin
from .permissions import OwnerRequiredMixin, StaffRequiredMixin


# ======Payment Account views start here=========
class PaymentAccountCreateView(LoginRequiredMixin, CreateView):
    form_class = vacancy_forms.PaymentAccountCreationForm
    template_name = 'vacancy_app/payment_account_form.html'

    # владелец компании текущий пользователь
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PaymentAccountDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
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

    def form_valid(self, form, **kwargs):
        # Protected DeleteView handler
        if self.object.company_list.count() > 0:
            messages.add_message(self.request, messages.ERROR,
                                 f"Can't be deleted, has {self.object.company_list.count()} children")
            return redirect('vacancy:payment_account_list')
        return super().form_valid(form)


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
    paginate_by = 5
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

    # владелец компании текущий пользователь
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CompanyDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = vacancy_models.Company


class CompanyListView(LoginRequiredMixin, ListView):
    model = vacancy_models.Company

    def get_queryset(self):
        queryset = vacancy_models.Company.objects.filter(owner=self.request.user)
        return queryset


class CompanyUpdateView(LoginRequiredMixin, RequestFormKwargsMixin, OwnerRequiredMixin, UpdateView):
    form_class = vacancy_forms.CompanyCreationForm
    model = vacancy_models.Company
    template_name = 'vacancy_app/company_form.html'


class CompanyDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = vacancy_models.Company
    success_url = reverse_lazy("vacancy:company_list")

    def form_valid(self, form, **kwargs):
        # Protected DeleteView handler
        if self.object.vacancy_list.count() > 0:
            messages.add_message(self.request, messages.ERROR,
                                 f"Can't be deleted, has {self.object.vacancy_list.count()} children")
            return redirect('vacancy:company_list')
        return super().form_valid(form)


# ===============Vacancy views start here=====================
class VacancyCreateView(LoginRequiredMixin, RequestFormKwargsMixin, CreateView):
    form_class = vacancy_forms.VacancyCreationForm
    template_name = 'vacancy_app/vacancy_form.html'

    # владелец компании текущий пользователь
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class VacancyDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = vacancy_models.Vacancy

    def get_queryset(self):
        queryset = super(VacancyDetailView, self).get_queryset()
        queryset = queryset.select_related('owner')
        return queryset


class VacancyListView(LoginRequiredMixin, ListView):
    paginate_by = 4
    model = vacancy_models.Vacancy

    def get_queryset(self):
        queryset = super(VacancyListView, self).get_queryset()
        queryset = queryset.filter(owner=self.request.user).select_related('company')
        return queryset


class VacancyUpdateView(LoginRequiredMixin, RequestFormKwargsMixin, OwnerRequiredMixin, UpdateView):
    form_class = vacancy_forms.VacancyCreationForm
    model = vacancy_models.Vacancy
    template_name = 'vacancy_app/vacancy_form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        # Если вакансия заблокирована пользователь не может менять статус
        if obj.status == vacancy_models.Vacancy.Status.BLOCKED:
            raise PermissionDenied()
        return obj


class VacancyDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = vacancy_models.Vacancy
    success_url = reverse_lazy("vacancy:vacancy_list")


# ========== Job List View for template==============
class JobsListView(ListView):
    paginate_by = 3
    model = vacancy_models.Vacancy
    template_name: str = "vacancy_app/job_listing.html"

    def get_queryset(self):
        """
        custom filter for url. url example
        # http://localhost:8000/vacancy/job-listing/?job-title=&job-location=&job-salary-from=1000&
        selected-applicant-level=2&selected-employment-type=3&selected-job-type=1#job-section
        """
        queryset = super(JobsListView, self).get_queryset()
        params = self.get_params_from_url()
        if params["job_title"]:
            queryset = queryset.filter(name__icontains=params["job_title"])
        if params["job_location"]:
            queryset = queryset.filter(location__icontains=params["job_location"])
        if params["job_salary_from"]:
            queryset = queryset.filter(
                Q(salary_from__gte=params["job_salary_from"]) | Q(salary_to__gte=params["job_salary_from"]))
        if params["selected_applicant_level"]:
            queryset = queryset.filter(applicant_level=params["selected_applicant_level"])
        if params["selected_employment_type"]:
            queryset = queryset.filter(employment_type=params["selected_employment_type"])
        if params["selected_job_type"]:
            queryset = queryset.filter(job_type=params["selected_job_type"])
        queryset = queryset.filter(status=vacancy_models.Vacancy.Status.ACTIVE).prefetch_related(
            "applicant_level", "employment_type", "job_type")
        return queryset

    def get_params_from_url(self):
        job_title = self.request.GET.get("job-title", None)
        job_location = self.request.GET.get("job-location", None)
        job_salary_from = self.request.GET.get("job-salary-from", None)
        selected_applicant_level = int(self.request.GET.get("selected-applicant-level", 0))
        selected_employment_type = int(self.request.GET.get("selected-employment-type", 0))
        selected_job_type = int(self.request.GET.get("selected-job-type", 0))

        params = {
            "job_title": job_title,
            "job_location": job_location,
            "job_salary_from": job_salary_from,
            "selected_applicant_level": selected_applicant_level,
            "selected_employment_type": selected_employment_type,
            "selected_job_type": selected_job_type,
        }
        return params

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(JobsListView, self).get_context_data()
        applicant_level = vacancy_models.ApplicantLevel.objects.all()
        employment_type = vacancy_models.EmploymentType.objects.all()
        job_type = vacancy_models.JobType.objects.all()
        context.update({'applicant_level': applicant_level, 'employment_type': employment_type, 'job_type': job_type})

        # Передаем get параметры формы из url назад в форму
        for param, value in self.get_params_from_url().items():
            if value:
                context.update({param: value})
        return context


class JobsDetailView(DetailView):
    model = vacancy_models.Vacancy
    template_name: str = "vacancy_app/job_details.html"

    def get_queryset(self):
        queryset = super(JobsDetailView, self).get_queryset()
        queryset = queryset.filter(status=vacancy_models.Vacancy.Status.ACTIVE).select_related('company')
        return queryset


# ===========Vacancy Moderation views start here=========
class SearchResultVacancyModerationListView(LoginRequiredMixin, StaffRequiredMixin, FilterView):
    paginate_by = 5
    model = vacancy_models.Vacancy
    template_name = 'vacancy_app/vacancy_moderation_search_results.html'
    filterset_class = VacancyFilter
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = super(SearchResultVacancyModerationListView, self).get_queryset()
        queryset = queryset.select_related("owner").order_by('-created_at')
        return queryset


class VacancyModerationUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    form_class = vacancy_forms.VacancyModerationCreationForm
    model = vacancy_models.Vacancy
    template_name = 'vacancy_app/vacancy_moderation_form.html'
    success_url = reverse_lazy("vacancy:vacancy_moderation_list")
