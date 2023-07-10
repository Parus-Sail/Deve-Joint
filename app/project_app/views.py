from typing import Any

from django.contrib import messages
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Prefetch
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View, generic
from django.views.generic.edit import ModelFormMixin
from rules import is_authenticated
from rules.contrib.views import PermissionRequiredMixin

from .forms import ProjectForm
from .models import Group, Membership, Project
from .rules import is_project_owner
from .service import MembershipService, ProjectService

User: type[AbstractBaseUser] = get_user_model()

# ============================================ PROJECTS =============================================

from django.contrib.auth.mixins import LoginRequiredMixin
from rules.contrib.views import PermissionRequiredMixin, permission_required


class ProjectListView(generic.ListView):
    model = Project
    template_name = 'project_app/project_list.html'
    context_object_name = 'projects'


class ProjectDetailView(generic.DetailView):
    template_name = 'project_app/project_detail.html'
    context_object_name = 'project'
    pk_url_kwarg = 'project_id'

    def get_queryset(self) -> QuerySet:
        """ Исключаем из выборки не принятых участников проекта """
        project_id = int(self.kwargs['project_id'])
        qs_members = Membership.objects.filter(waiting_status=None, project_id=project_id)
        pre_qs_members = Prefetch('memberships', queryset=qs_members)
        res = Project.objects.filter(pk=project_id).prefetch_related(pre_qs_members)

        return res


# LoginRequiredMixin,
class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    # success_url —> to project_app:detail
    model = Project
    template_name = 'project_app/project_form.html'
    form_class = ProjectForm
    permission_required = "auth_user"

    def form_valid(self, form):
        # owner_id = int(self.request.user.id)
        owner_id = int(get_user(self.request).id)
        self.object: Project = ProjectService.create_project(owner_id, **form.cleaned_data)
        # пропоускаем стандарную реализацию сохранения объекта в БД, переходим сразу к редиректу
        return super(ModelFormMixin, self).form_valid(form)


# @permission_required('project_app.change_project', fn=is_project_owner)
class ProjectUpdateView(PermissionRequiredMixin, generic.UpdateView):
    # success_url —> to project_app:detail
    model = Project
    template_name = 'project_app/project_form.html'
    pk_url_kwarg = 'project_id'
    form_class = ProjectForm
    permission_required = "project_owner"
    raise_exception = True

    def get_permission_object(self):
        return self.get_object()

    def form_valid(self, form):
        project_id = int(self.kwargs['project_id'])
        self.object: Project = ProjectService.update_project(project_id, **form.cleaned_data)
        # пропоускаем стандарную реализацию сохранения объекта в БД, переходим сразу к редиректу
        return super(ModelFormMixin, self).form_valid(form)


class ProjectDeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = Project
    template_name = 'project_app/project_delete.html'
    success_url = reverse_lazy('project_app:list')
    pk_url_kwarg = 'project_id'
    permission_required = "project_owner"

    def form_valid(self, form):
        project_id = int(self.kwargs[self.pk_url_kwarg])
        ProjectService.delete_project(project_id)
        return redirect(self.get_success_url())

    # def form_valid(self, form):
    # def delete(self, request, *args, **kwargs):
    #     self.pk = int(self.kwargs['project_id'])
    #     ProjectService.delete_project(self.pk)
    #     return super().delete(request, *args, **kwargs)


class MyProjectsView(generic.ListView):
    template_name = 'project_app/my_projects.html'
    pk_url_kwarg = 'project_id'
    context_object_name = 'projects'

    def get_queryset(self):
        """ Owner's projects """
        return get_user(self.request).projects.all()


# ============================================= MEMBERS =============================================


class ListProjectMembersView(generic.ListView):
    template_name = 'project_app/projects_members.html'
    pk_url_kwarg = 'project_id'
    context_object_name = 'members'

    def get_queryset(self) -> QuerySet:
        """ оптимизация запроса (получение всех пользователей за раз)"""
        project_id = int(self.kwargs['project_id'])
        qs_users = User.objects.filter(memberships__project_id=project_id)
        pre_qs_users = Prefetch('user', queryset=qs_users)
        return Membership.objects.filter(project_id=project_id).prefetch_related(pre_qs_users)


# ============================================= приглашение от участника ============================


class InviteToProjectView(PermissionRequiredMixin, View):
    permission_required = ["project_member", "project_owner"]

    def get(self, request, user_id, project_id):
        """ участник предлагает вступить в проект """
        member_id = self.request.user.id

        MembershipService.suggest_membership(user_id, member_id, project_id)
        messages.success(request, "Invitation sent")
        return redirect('invite')


class ApproveMemberView(PermissionRequiredMixin, View):
    permission_required = "project_not_member"

    def get(self, request, project_id):
        """ пользователь соглашется вступить в проект """
        user_id = self.request.user.id

        MembershipService.approve_membership(user_id, project_id)
        messages.success(request, "Member approved")
        return redirect('approve')


class DisapproveMemberView(PermissionRequiredMixin, View):
    permission_required = "project_not_member"

    def get(self, request, project_id, user_id):
        """ пользователь отказывается вступить в проект """
        user_id = self.request.user.id

        MembershipService.disapprove_membersip(user_id, project_id)
        messages.success(request, "Member disapproved")
        return redirect('disapprove')


# ============================================= заявление от желающего вступить =====================


class ApplicationMemberView(PermissionRequiredMixin, View):
    permission_required = "project_not_member"

    def get(self, request, project_id):
        """ пользователь отправляет заявку на участие в проекте """
        applicant_id = self.request.user.id

        MembershipService.application_by_user(applicant_id, project_id)
        messages.success(request, "Application submitted")
        return redirect('application')


class AcceptMemberView(PermissionRequiredMixin, View):
    permission_required = "project_owner"

    def get(self, request, project_id, applicant_id):
        """ руководитель принимает заявку на участие """
        # owner_id = self.request.user.id

        MembershipService.accept_member(applicant_id, project_id)
        messages.success(request, "Member accepted")
        return redirect('accept')


class RejectMemberView(PermissionRequiredMixin, View):
    permission_required = "project_owner"

    def get(self, request, project_id, applicant_id):
        """ руководитель отклоняет заявку на участие """
        # owner_id = self.request.user.id

        MembershipService.reject_member(applicant_id, project_id)
        messages.success(request, "Member rejected")
        return redirect('reject')


# ============================================= исключение и выход =====================

# class DisapproveMemberView(View):

#     def post(self, request, project_id, user_id):
#         """ пользователь отказывается вступить в проект """
#         user_id = self.request.user.id

#         MembershipService.disapprove_membersip(user_id, project_id)
#         messages.success(request, "Member disapproved")
#         return redirect('disapprove')