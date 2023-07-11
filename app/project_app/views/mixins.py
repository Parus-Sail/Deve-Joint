from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Prefetch
from django.db.models.query import QuerySet

from ..models import Membership, Owner, Project

# from .. import forms

User: type[AbstractBaseUser] = get_user_model()

# ============================================= OWNER MIXINS =============================================


class OwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    """ Предоставляет выборку собственных объектов и запрящает доступ к чужим """

    def get_queryset(self) -> QuerySet:
        """ Выборка принадлежащая пользователю """
        qs: QuerySet = super().get_queryset()
        # обязательно наличие атрибута owner у модели
        if not hasattr(qs.model, 'owner'):
            raise AttributeError('Model don\'t have owner attribute')
        return qs.filter(owner=get_user(self.request))

    def test_func(self) -> bool:
        """ Проверяем является ли текущий пользователь собственником конкретного объекта (для UpdateViews, DeleteViews) """
        # todo: не поддерживается slug
        obj_pk = self.kwargs.get(self.pk_url_kwarg)
        if obj_pk:
            user = get_user(self.request)
            return Owner.is_owning(user, obj_pk)
        return True


class OwnerEditMixin(LoginRequiredMixin):
    """ Добавляем для каждого экземпляра модели — собственника, при отправке формы """

    def form_valid(self, form):
        # обязательно наличие атрибута owner у модели
        if not hasattr(form.instance, 'owner'):
            raise AttributeError('Model don\'t have owner attribute')

        form.instance.owner = get_user(self.request)
        return super().form_valid(form)


# ============================================= PROJECTS MIXIN ===========================================


class ProjectMixin:
    """ Предоставляет доступ к модели проектов """
    model = Project
    pk_url_kwarg: str = 'project_id'


class OwnProjectMixin(OwnerMixin, ProjectMixin):
    """ Ограничивает доступ в рамках только своих проектов """


class OwnProjectEditMixin(OwnProjectMixin, OwnerEditMixin):
    """ Помечаем все новые проекты, как свои и ограничивам в их рамках свой доступ """
    # form_class = ProjectForm # todo: включить после тестов
    fields = ['title', 'description']


# ============================================= MEMBER MIXIN =============================================


class WithAllMembershipMixin:
    """ Предоставляет выборку ВСЕХ участников проекта (с оптимизацией запроса) """

    def get_queryset(self) -> QuerySet:
        project_qs: QuerySet = super().get_queryset()

        projects_qs_with_all_members = project_qs.prefetch_related('memberships', 'memberships__user')
        return projects_qs_with_all_members


class WithActiveMembershipMixin:
    """ Предоставляет выборку только АКТИВНЫХ (подтвержденных) участников проекта (с оптимизацией запроса) """

    def get_queryset(self) -> QuerySet:

        members_qs = Membership.objects.filter(active=True)
        members_pre_qs = Prefetch('memberships', queryset=members_qs)

        projects_qs = super().get_queryset()
        projects_qs_wtih_active_members: QuerySet = projects_qs.prefetch_related(members_pre_qs)

        return projects_qs_wtih_active_members