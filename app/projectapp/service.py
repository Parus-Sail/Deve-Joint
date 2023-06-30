from django.db import transaction
from projectapp.models import Membership, Project
from roleapp.models import Role

from .models import Membership, Project


@transaction.atomic
def create_project(title: str, description: str, owner):

    project = Project.objects.create(
        title=title,
        description=description,
        owner=owner,
    )

    admin_role, created = Role.objects.get_or_create(name='admin')

    founder = Membership.objects.create(
        project=project,
        user=owner,
        role=admin_role,
    )

    return project


@transaction.atomic
def delete_project(project):
    project.delete()


@transaction.atomic
def update_project(project, **kwargs):
    for key, value in kwargs.items():
        setattr(project, key, value)
    project.save()


@transaction.atomic
def include_member(project, user, role):
    membership = Membership.objects.create(project=project, user=user, role=role)
    return membership


@transaction.atomic
def exclude_member(project, user):
    membership = Membership.objects.get(project=project, user=user)
    membership.delete()
