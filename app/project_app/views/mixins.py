from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Prefetch
from django.db.models.query import QuerySet
from django.views import View

from .. import forms
from ..models import Membership, Owner, Project

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

from favorite_app.models import FavoriteProjects

from ..models import Project


class ProjectMixin:
    """ Предоставляет доступ к модели проектов """
    model = Project
    pk_url_kwarg: str = 'project_id'

    def get_context_data(self, **kwargs):
        # todo: refactor Favorites to came to way single responsibility
        context: dict = super().get_context_data(**kwargs)
        favorites_of_user = FavoriteProjects.objects.filter(user=self.request.user.id)
        favorites_pk_list = [item.project.pk for item in favorites_of_user]
        context["favorites_pk_list"] = favorites_pk_list
        return context


class OwnProjectMixin(OwnerMixin, ProjectMixin):
    """ Ограничивает доступ в рамках только своих проектов """


class OwnProjectEditMixin(OwnProjectMixin, OwnerEditMixin):
    """ Помечаем все новые проекты, как свои и ограничивам в их рамках свой доступ """
    form_class = forms.ProjectForm  # todo: включить после тестов

    # fields = ['title', 'description']


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


# ===================================== EXPERIMENTS =====================================================


class IncludeToProjectMixit(LoginRequiredMixin):  #todo: implement
    """
	реализует логику добавления пользователя в проект, как участника.
	получает атрибуты в POST request: user_id_to_add и project_id
	"""


class ExcludeFromProjectMixin(LoginRequiredMixin):  #todo: implement
    """
	реализует логику исключения пользователя из участников проекта.
	получает атрибуты в POST request: user_id_to_add и project_id
	"""


class LeaveProjectView(ExcludeFromProjectMixin, View):  #todo: implement
    """ Участник проекта выходит из него """


class KickOutFromProjectView(OwnerMixin, ExcludeFromProjectMixin, View):  #todo: implement
    """ Участник проекта выходит из него """


class NotMember(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self) -> bool:
        """ проверяем является ли текущий пользователь участником проекта """
        # todo: не поддерживается slug
        project_pk = self.kwargs.get(self.pk_url_kwarg)
        if project_pk:
            user = get_user(self.request)
            return Owner.is_owning(user, project_pk)
        return True


# todo: think about events that are suitable for maintaining a single resonant ability
#
# def project_application(user: User, project: Project) -> Membership:
#
# send_message(project.owner: User, sender: User, title, text)
# > message: Message = message_factory(title, text)
# > sender.outbox(recipient: User, message)
# > recipient.inbox(sender: User, message)
#
# or like event
#
# application_to_project_event = Application(user, project)
# ...
#
# envent_bus(application_to_project_event: Envet)
# envent_bus(reject_application_to_project_event: Envet)
# envent_bus(accept_application_to_project_event: Envet)
#
# in envent module:
# events: dict[Event, list[handlers]]
# event_bus.handle(event)
#
# event_bus.handle(event) — in envent module
#
# membership = Membership.objects.create(user=user, project=project)
# return membership
