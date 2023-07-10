from django import http
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.db import transaction
from django.db.models import Prefetch, QuerySet
from django.shortcuts import get_object_or_404

from .models import Membership, Project

User: type[AbstractBaseUser] = get_user_model()

# @transaction.atomic
# def create_project(owner: User, **kwargs) -> Project:
#     project = Project.objects.create(owner=owner, **kwargs)
#     project.memberships.create(user=owner)
#     return project

# @transaction.atomic
# def update_project(project: Project, **kwargs) -> Project:
#     for key, value in kwargs.items():
#         setattr(project, key, value)
#     project.save()

# def delete_project(project: Project) -> None:
#     project.delete()

# def include_member(project, user):
#     membership = Membership.objects.create(project=project, user=user, role=role)
#     return membership

# @transaction.atomic
# def include_member(project, user):
#     membership = Membership.objects.create(project=project, user=user, role=role)
#     return membership

# @transaction.atomic
# def exclude_member(project, user):
#     membership = Membership.objects.get(project=project, user=user)
#     membership.delete()

# ================================================================================================================================================================


class ProjectService:

    @staticmethod
    @transaction.atomic
    def create_project(owner_id: int, **kwargs_from_form) -> Project:
        owner = get_object_or_404(User, pk=owner_id)
        project = Project.objects.create(owner=owner, **kwargs_from_form)
        MembershipService._include_member(owner_id, project.id)
        return project

    @staticmethod
    def update_project(project_id: int, **kwargs_from_form) -> Project:
        project = get_object_or_404(Project, pk=project_id)
        for key, value in kwargs_from_form.items():
            setattr(project, key, value)
        project.save()
        return project

    @staticmethod
    def delete_project(project_id: int) -> None:
        project = get_object_or_404(Project, pk=project_id)
        project.delete()


class MembershipService:

    @staticmethod
    def _include_member(user_id: int, project_id: int, waiting_status=None):
        user: AbstractBaseUser = get_object_or_404(User, pk=user_id)
        project: Project = get_object_or_404(Project, pk=project_id)

        membership, created = Membership.objects.get_or_create(user=user, project=project)
        if waiting_status:
            membership.waiting_status = waiting_status
            membership.save()

    @staticmethod
    def _exclude_member(user_id: int, project_id: int):
        user: AbstractBaseUser = get_object_or_404(User, pk=user_id)
        project: Project = get_object_or_404(Project, pk=project_id)

        membership = get_object_or_404(Membership, user=user, project=project)
        membership.delete()

# ============================================= приглашение от участника ============================

    @staticmethod
    def suggest_membership(user_id: int, member_id: int, project_id: int):
        MembershipService._include_member(user_id, project_id, waiting_status='wait_user')

    @staticmethod
    def approve_membership(user_id: int, project_id: int):
        MembershipService._include_member(user_id, project_id, waiting_status=None)

    @staticmethod
    def disapprove_membersip(user_id: int, project_id: int):
        MembershipService._exclude_member(user_id, project_id)

# ============================================= заявление от желающего вступить =====================

    @staticmethod
    def application_by_user(applicant_id: int, project_id: int):
        MembershipService._include_member(applicant_id, project_id, waiting_status='wait_owner')

    @staticmethod
    def accept_application(applicant_id: int, project_id: int):
        MembershipService._include_member(applicant_id, project_id, waiting_status=None)

    @staticmethod
    def reject_application(applicant_id: int, project_id: int):
        MembershipService._exclude_member(applicant_id, project_id)


# ================================================================================================================================================================

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
