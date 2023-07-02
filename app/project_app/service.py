from django.db import transaction
from django.db.models import QuerySet
from project_app.models import Membership, Project
from role_app.models import Role

from .models import Membership, Project


def project_list() -> QuerySet:
    return Project.objects.all()


@transaction.atomic
def create_project(title: str, description: str, owner) -> Project:

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
def delete_project(project_pk: int):
    Project.objects.get(id=project_pk).delete()


@transaction.atomic
def update_project(project_pk: int, **kwargs):
    project = Project.objects.get(id=project_pk)
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
