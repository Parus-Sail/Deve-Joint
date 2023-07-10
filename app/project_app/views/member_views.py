from django.contrib import messages
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Prefetch
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View, generic
from django.views.generic import FormView
from django.views.generic.edit import ModelFormMixin

from ..models import Member, Membership, Owner, Project
from .project_views import OwnerMixin

# from .service import MembershipService, ProjectService

User: type[AbstractBaseUser] = get_user_model()


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


# ============================================= приглашение от участника ============================


class InviteToProjectView(LoginRequiredMixin, View):  #todo: implement
    """ участник проекта предлагает НЕ участнику (пользователю) вступить в проект """

    def post(self, request):

        try:
            invited_user_id: int = int(request.GET.get('user_id'))
            invited_user = User.objects.get(id=invited_user_id)

            project_id: int = int(request.GET.get('project_id'))
            project: Project = Project.objects.get(id=project_id)

            action: int = int(request.GET.get('aciton'))
            member = Member(request.user)

            if Member.objects.first(user=invited_user):
                raise Exception('User already take a part in the project')

            # match action:
            #     case 'create':

        except:
            pass

        # Проверка, что текущий пользователь является владельцем проекта
        # if project.owner != request.user:
        # raise PermissionDenied

        # Логика добавления пользователя в проект

        return JsonResponse({'status': 'ok'})

        member_id = self.request.user.id

        MembershipService.suggest_membership(user_id, member_id, project_id)
        messages.success(request, "Invitation sent")
        return redirect('invite')


# class DecisionOfInviteView(View):  #todo: implement
#     """ НЕ участник проекта (пользователь) соглашется или не соглашается вступить в проект """

#     def post(self, request, project_id):

#         if request:
#             user_id = self.request.user.id

#             MembershipService.approve_membership(user_id, project_id)
#             messages.success(request, "Member approved")
#             return redirect('approve')
#         else:
#             # пользователь отказывается вступить в проект
#             user_id = self.request.user.id

#             MembershipService.disapprove_membersip(user_id, project_id)
#             messages.success(request, "Member disapproved")
#             return redirect('disapprove')

# # ============================================= заявление от желающего вступить =====================

# class ApplicationMemberView(View):  #todo: implement
#     """ пользователь (НЕ участник проекта) отправляет заявку на участие в проекте """

#     def post(self, request, project_id):

#         applicant_id = self.request.user.id

#         MembershipService.application_by_user(applicant_id, project_id)
#         messages.success(request, "Application submitted")
#         return redirect('application')

# class DecisionOfApplicationView(View):  #todo: implement
#     """ руководитель принимает заявку на участие """

#     def post(self, request, project_id, applicant_id):
#         if request:
#             # owner_id = self.request.user.id

#             MembershipService.accept_member(applicant_id, project_id)
#             messages.success(request, "Member accepted")
#             return redirect('accept')

#         else:
#             #  руководитель отклоняет заявку на участие
#             # owner_id = self.request.user.id

#             MembershipService.reject_member(applicant_id, project_id)
#             messages.success(request, "Member rejected")
#             return redirect('reject')

# =======================================================================================

# todo: delete later
# def get_queryset(self) -> QuerySet:
#     project_id = int(self.kwargs['project_id'])
#     qs_members = Membership.objects.filter(waiting_status=None, project_id=project_id)
#     pre_qs_members = Prefetch('memberships', queryset=qs_members)
#     res = Project.objects.filter(pk=project_id).prefetch_related(pre_qs_members)
#     return res

# =======================================================================================

# todo: delete later
# class ListProjectMembersView(ProjectMixin, generic.ListView):
#     template_name_suffix = 'members_own_detail.html'

#     pk_url_kwarg = 'project_id'
#     context_object_name = 'members'

#     def get_queryset(self) -> QuerySet:
#         """ оптимизация запроса (получение всех пользователей за раз)"""
#         project_id = int(self.kwargs['project_id'])
#         qs_users = User.objects.filter(memberships__project_id=project_id)
#         pre_qs_users = Prefetch('user', queryset=qs_users)
#         return Membership.objects.filter(project_id=project_id).prefetch_related(pre_qs_users)