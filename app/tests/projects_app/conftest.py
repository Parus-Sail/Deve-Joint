# #todo why not working: from django.contrib.auth import get_user_model
from authapp.models import BaseOpenSailUser as User
from projects_app.models import Project
import pytest
from roles_app.models import Role


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpassword',
        email='testemail@example.com',
    )


@pytest.fixture
def user_second():
    return User.objects.create_user(
        username='testuser_2',
        password='testpassword',
        email='testemail_2@example.com',
    )


@pytest.fixture
def project(user):
    return Project.objects.create(title='Test Project', description='Test Description', owner=user)


@pytest.fixture
def role():
    return Role.objects.create(name='Test Role')