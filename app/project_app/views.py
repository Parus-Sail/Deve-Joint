from typing import Any

from django.contrib import messages
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import ModelFormMixin

from . import models, service
from .forms import ProjectCreationForm

User = get_user_model()


class ProjectListView(generic.ListView):
    queryset = service.project_list()
    template_name = 'project_app/project_list.html'
    context_object_name = 'projects'


class ProjectDetailView(generic.DetailView):
    queryset = service.project_list()
    template_name = 'project_app/project_detail.html'
    context_object_name = 'project'


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Project
    template_name = 'project_app/create_project.html'
    form_class = ProjectCreationForm

    def form_valid(self, form):
        self.object = project = service.create_project(
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],
            owner=get_user(self.request),
        )

        # write message for example
        # messages.success(self.request, 'Project created successfully!')

        self.success_url = reverse_lazy("project_app:detail", kwargs={"pk": project.pk})
        # пропоускаем стандарную реализацию сохранения объекта в БД, переходим сразу к редиректу
        return super(ModelFormMixin, self).form_valid(form)


# STUB
class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Project
    template_name = 'project_app/project_update.html'
    context_object_name = 'project'
    fields = 'title', 'description'

    def form_valid(self, form):
        service.update_project(self.object,
                               title=form.cleaned_data['title'],
                               description=form.cleaned_data['description'])
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)


# STUB
class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
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
