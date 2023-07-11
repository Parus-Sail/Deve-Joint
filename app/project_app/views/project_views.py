from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.urls import reverse_lazy
from django.views import generic

from .mixins import (
    OwnProjectEditMixin,
    OwnProjectMixin,
    ProjectMixin,
    WithActiveMembershipMixin,
    WithAllMembershipMixin,
)

User: type[AbstractBaseUser] = get_user_model()

# ============================================= PROJECTS =================================================


class ProjectListView(ProjectMixin, generic.ListView):
    """ Список всех проектов  """


class ProjectDetailView(ProjectMixin, WithActiveMembershipMixin, generic.DetailView):
    """ Конкретный проект с АКТИВНЫМИ (подтвержденными) участникми """


# ============================================= OWN PROJECTS =============================================


class OwnProjectListView(OwnProjectMixin, generic.ListView):
    """ Спиосок собтсвеных проектов """
    template_name_suffix = '_own_list'


class OwnProjectDetail(OwnProjectMixin, WithAllMembershipMixin, generic.DetailView):
    """ Конкретный проект со ВСЕМИ участникми (на рассмотрении) """
    template_name_suffix = '_own_detail'


class OwnProjectCreateView(OwnProjectEditMixin, generic.CreateView):
    """ Создаем проект указываем себя как собтсвенника и участника """


class OwnProjectUpdateView(OwnProjectEditMixin, generic.UpdateView):
    """ Получаем доступ к редактированию СВОЕГО проекта """


class OwnProjectDeleteView(OwnProjectMixin, generic.DeleteView):
    """ Получаем доступ к удалению СВОЕГО проекта """
    success_url = reverse_lazy('project_app:list')
