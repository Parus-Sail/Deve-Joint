from typing import Any

from django.contrib import messages
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import ModelFormMixin
from favorite_app.models import FavoriteProjects

from . import forms, models, permissions, service

User = get_user_model()


class ProjectListView(generic.ListView):
    queryset = service.project_list()
    template_name = 'project_app/project_list.html'
    context_object_name = 'projects'


class ProjectDetailView(generic.DetailView):
    queryset = service.project_list()
    template_name = 'project_app/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(models.Project, pk=self.kwargs['pk'])
        is_in_favorites = FavoriteProjects.objects.filter(user=self.request.user, project=project)
        context["is_in_favorites"] = is_in_favorites
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Project
    template_name = 'project_app/project_form.html'
    form_class = forms.ProjectCreateForm

    def form_valid(self, form):
        self.object = project = service.create_project(
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],
            owner=get_user(self.request),
        )

        # write message for example
        # messages.success(self.request, 'Project created successfully!')

        self.success_url = reverse_lazy("project_app:detail", kwargs={"pk": self.object.pk})
        # пропоускаем стандарную реализацию сохранения объекта в БД, переходим сразу к редиректу
        return super(ModelFormMixin, self).form_valid(form)


class ProjectUpdateView(
        LoginRequiredMixin,
        permissions.OwnerRequiredMixin,
        generic.UpdateView,
):
    model = models.Project
    template_name = 'project_app/project_form.html'
    context_object_name = 'project'
    fields = 'title', 'description'

    def form_valid(self, form):
        self.object = service.update_project(
            self.object,
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],
        )

        self.success_url = reverse_lazy("project_app:detail", kwargs={"pk": self.object.pk})
        # пропоускаем стандарную реализацию сохранения объекта в БД, переходим сразу к редиректу
        return super(ModelFormMixin, self).form_valid(form)


class ProjectDeleteView(
        LoginRequiredMixin,
        permissions.OwnerRequiredMixin,
        generic.DeleteView,
):
    model = models.Project
    template_name = 'project_app/project_delete.html'
    success_url = reverse_lazy('list_projects')

    def delete(self, request, *args, **kwargs):
        service.delete_project(self.object)
        messages.success(self.request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Owner's projects
class MyProjectsView(generic.ListView):
    template_name = 'project_app/my_projects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return models.Project.objects.filter(owner=get_user(self.request))
