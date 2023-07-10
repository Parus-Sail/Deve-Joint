from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Prefetch
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views import generic

# from .. import forms
from ..models import Membership, Project

User: type[AbstractBaseUser] = get_user_model()

# ============================================= OWNER MIXINS =============================================


class OwnerMixin(LoginRequiredMixin):
    """ Выборка принадлежащая пользователю """

    def get_queryset(self) -> QuerySet:
        qs: QuerySet = super().get_queryset()

        # обязательно наличие атрибута owner у модели
        if not hasattr(qs.model, 'owner'):
            raise AttributeError('Model don\'t have owner attribute')
        return qs.filter(owner=get_user(self.request))


class OwnerEditMixin(LoginRequiredMixin):
    """ Перед сохранением экземпляра модели добавляет экземпляр текущего пользователя, как владельца """

    def form_valid(self, form):
        # обязательно наличие атрибута owner у модели
        if not hasattr(form.instance, 'owner'):
            raise AttributeError('Model don\'t have owner attribute')

        form.instance.owner = get_user(self.request)
        return super().form_valid(form)


# ============================================= PROJECTS MIXIN ===========================================


class ProjectMixin:
    model = Project
    pk_url_kwarg: str = 'project_id'


class OwnProjectMixin(OwnerMixin, ProjectMixin):
    pass


class OwnProjectEditMixin(OwnProjectMixin, OwnerEditMixin):
    # form_class = ProjectForm
    fields = ['title', 'description']


class MembershipMixin:

    def get_queryset(self) -> QuerySet:
        """ Выборка всех участников проекта (с оптимизацией запроса) """
        project_qs: QuerySet = super().get_queryset()
        qs = project_qs.prefetch_related('memberships', 'memberships__user')
        return qs


class ActiveMembershipMixin(MembershipMixin):

    def get_queryset(self) -> QuerySet:
        """ Выборка активных участников проекта (с оптимизацией запроса) """
        project_qs_with_membership_and_user: QuerySet = super().get_queryset()
        return project_qs_with_membership_and_user.filter(memberships__active=True)


# ============================================= PROJECTS =================================================


class ProjectListView(ProjectMixin, generic.ListView):
    pass


class ProjectDetailView(ProjectMixin, ActiveMembershipMixin, generic.DetailView):
    """ Имеется возможность просматривать только активных участников """


# ============================================= OWN PROJECTS =============================================


class OwnProjectListView(OwnProjectMixin, generic.ListView):
    template_name_suffix = '_own_list'


class OwnProjectDetail(OwnProjectMixin, MembershipMixin, generic.DetailView):
    """ Имеется возможность просматривать всех участников (в том числе и не активных) """
    template_name_suffix = '_own_detail'


class OwnProjectCreateView(OwnProjectEditMixin, generic.CreateView):
    pass


class OwnProjectUpdateView(OwnProjectEditMixin, generic.UpdateView):
    pass


class OwnProjectDeleteView(OwnProjectMixin, generic.DeleteView):
    success_url = reverse_lazy('project_app:list')  # todo: нужна ли переменная?


# ============================================= MEMBERS ==================================================

# ============================================= исключение и выход =====================
