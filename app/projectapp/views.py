from django.contrib import messages
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from . import models, service

User = get_user_model()


class ProjectListView(generic.ListView):
    queryset = service.project_list()
    template_name = 'projectapp/project_list.html'
    context_object_name = 'projects'


class ProjectDetailView(generic.DetailView):
    queryset = service.project_list()
    template_name = 'projectapp/project_detail.html'
    context_object_name = 'project'


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Project
    template_name = 'projectapp/create_project.html'
    fields = 'title', 'description'

    def form_valid(self, form):
        project = service.create_project(
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],
            owner=get_user(self.request),
        )

        # write message for example
        # messages.success(self.request, 'Project created successfully!')

        # пропоускаем стандарную реализацию сохранения объекта в БД, переходим сразу к редиректу
        self.success_url = reverse_lazy("projectapp:detail", kwargs={"pk": project.pk})
        return super().form_valid(form)


# STUB
class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Project
    template_name = 'projectapp/update_project.html'
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
    template_name = 'projectapp/delete_project.html'
    success_url = reverse_lazy('list_projects')

    def delete(self, request, *args, **kwargs):
        service.delete_project(self.object)
        messages.success(self.request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)