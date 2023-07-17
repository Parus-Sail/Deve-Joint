from django.conf import settings
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from . import forms, models

UserModel = get_user_model()


class CVListView(ListView):
    template_name: str = "cv_app/cv_list.html"
    model = models.CV
    context_object_name = 'cv_list'
    paginate_by = settings.DEFAULT_PAGINATE_SIZE
    queryset = models.CV.objects.filter(is_published=True)


class UserCVListView(ListView, LoginRequiredMixin):
    model = models.CV
    context_object_name = 'cv_list'
    template_name: str = "cv_app/cv_list.html"
    paginate_by = settings.DEFAULT_PAGINATE_SIZE

    def get_queryset(self):
        return models.CV.objects.filter(owner=get_user(self.request))


class CVDetailView(DetailView):
    model = models.CV
    context_object_name = 'cv'
    template_name = 'cv_app/cv_detail.html'


class CVCreateView(CreateView, LoginRequiredMixin):
    model = models.CV
    template_name = 'cv_app/cv_create_form.html'
    form_class = forms.CVCreationForm
    success_url = reverse_lazy("cv_app:my-cv-list")

    def form_valid(self, form):
        form.instance.owner = get_user(self.request)
        return super().form_valid(form)


class CVUpdateView(UpdateView, LoginRequiredMixin):
    model = models.CV
    template_name = 'cv_app/cv_update_form.html'
    form_class = forms.CVCreationForm
    success_url = reverse_lazy("cv_app:my-cv-list")

    def form_valid(self, form):
        form.instance.owner = get_user(self.request)
        return super().form_valid(form)


class CVDeleteView(DeleteView, LoginRequiredMixin):
    model = models.CV
    template_name = 'cv_app/cv_confirm_delete.html'
    context_object_name = 'cv'
    success_url = reverse_lazy("cv_app:my-cv-list")
