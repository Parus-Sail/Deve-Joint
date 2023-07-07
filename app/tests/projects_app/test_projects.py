from project_app.models import Membership, Project
from project_app.service import create_project, delete_project, exclude_member, include_member, update_project
import pytest


@pytest.mark.django_db
def test_create_project(user):
    project = create_project(owner=user, title='Test Project', description='Test Description')
    assert isinstance(project, Project)
    assert project.title == 'Test Project'
    assert project.description == 'Test Description'
    assert project.owner == user


@pytest.mark.django_db
def test_delete_project(project):
    delete_project(project.id)
    assert not Project.objects.filter(project_id=project.pk).exists()


@pytest.mark.django_db
def test_update_project(project):
    update_project(project.id, title='Updated Title', description='Updated Description')
    project.refresh_from_db()
    assert project.title == 'Updated Title'
    assert project.description == 'Updated Description'


@pytest.mark.django_db
def test_include_member(project, user_second, role):
    membership = include_member(project, user_second, role)
    assert isinstance(membership, Membership)
    assert membership.project == project
    assert membership.user == user_second
    assert membership.role == role
    exclude_member(project, user_second)


@pytest.mark.django_db
def test_exclude_member(project, user_second, role):
    include_member(project, user_second, role)
    exclude_member(project, user_second)
    assert not Membership.objects.filter(project=project, user=user_second).exists()
