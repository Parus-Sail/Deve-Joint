from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from main_app import models


class MainPageView(TemplateView):
    template_name: str = "main_app/index.html"


class ContactsPageView(TemplateView):
    template_name: str = "main_app/contacts.html"


class AboutPageView(TemplateView):
    template_name: str = "main_app/about.html"


# News views
class NewsListView(ListView):
    model = models.News
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = models.News
    fields = '__all__'
    success_url = reverse_lazy("main_app:news")
    permission_required = ("main_app.add_news")


class NewsDetailView(DetailView):
    model = models.News


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = models.News
    fields = '__all__'
    success_url = reverse_lazy("main_app:news")
    permission_required = ("main_app.change_news",)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = models.News
    success_url = reverse_lazy("main_app:news")
    permission_required = ("main_app.delete_news",)
