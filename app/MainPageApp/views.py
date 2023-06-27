from django.views.generic import TemplateView
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from MainPageApp import models


# Заготовки под вьюхи.


class MainPageView(TemplateView):
    template_name: str = "MainPageApp/index.html"


class ContactsPageView(TemplateView):
    template_name: str = "MainPageApp/contacts.html"


class AboutPageView(TemplateView):
    template_name: str = "MainPageApp/about.html"


class JobsListingView(TemplateView):
    template_name: str = "MainPageApp/job_listing.html"


class JobsDetailView(TemplateView):
    template_name: str = "MainPageApp/job_details.html"


# News views
class NewsListView(ListView):
    model = models.News
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = models.News
    fields = '__all__'
    success_url = reverse_lazy("MainPageApp:news")
    permission_required = ("MainPageApp.add_news",)


class NewsDetailView(DetailView):
    model = models.News


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = models.News
    fields = '__all__'
    success_url = reverse_lazy("MainPageApp:news")
    permission_required = ("MainPageApp.change_news",)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = models.News
    success_url = reverse_lazy("MainPageApp:news")
    permission_required = ("MainPageApp.delete_news",)
