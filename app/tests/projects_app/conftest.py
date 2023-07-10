# #todo why not working: from django.contrib.auth import get_user_model
from auth_app.models import BaseOpenSailUser as User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import RequestFactory
from project_app.models import Membership, Project

User = get_user_model()
import pytest
from rules import set_perm


def permission_factory(permission: str):
    return set_perm(permission, lambda _: True)
    # if rule_exists(permission):


@pytest.fixture(scope='function')
def guest_user() -> User:
    guest = User.objects.create_user(username='guest_user',
                                     password='password',
                                     email='guest_user@example.com',
                                     email_verify=True)
    return guest


@pytest.fixture(scope='function')
def auth_user(client) -> User:
    auth_user = User.objects.create_user(username='testuser',
                                         password='testpassword',
                                         email='test@example.com',
                                         email_verify=True)

    client.force_login(auth_user)
    permission_factory('auth_user')
    return auth_user


@pytest.fixture(scope='function')
def owner_user(client) -> User:
    owner = User.objects.create_user(username='owner_user',
                                     password='password',
                                     email='owner_user@example.com',
                                     email_verify=True)
    client.force_login(owner)
    permission_factory('project_owner')
    return owner


@pytest.fixture(scope='function')
def member_user(client) -> User:
    member = User.objects.create_user(username='member_user',
                                      password='password',
                                      email='member_user@example.com',
                                      email_verify=True)
    client.force_login(member)
    permission_factory('project_member')
    return member


@pytest.fixture(scope='function')
def project(owner_user) -> Project:
    project = Project.objects.create(title='Test Project', description='Test Description', owner=owner_user)
    Membership.objects.create(user=owner_user, project=project)
    return project


@pytest.fixture(scope='function')
def project_member(project, member_user) -> Membership:
    return Membership.objects.create(user=member_user, project=project)
