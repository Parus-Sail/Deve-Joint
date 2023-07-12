# # from project_app.service import create_project, delete_project, exclude_member, include_member, update_project
# from django.contrib.auth.models import Permission
# from django.core.exceptions import PermissionDenied
# # User = get_user_model()
# from django.test import RequestFactory
# from django.urls import reverse
# from project_app.models import Membership, Project
# # import rules
# from project_app.views import ListProjectMembersView
# import pytest
# from rules import add_perm

# # from django.contrib.auth import get_user_model

# @pytest.mark.django_db
# def test_auth_and_rules_for_user(guest_user, client):

#     # не авторизован и нет прав
#     url = reverse('project_app:create')
#     response = client.get(url)
#     assert response.status_code == 302

#     # авторизован и нет прав
#     url = reverse('project_app:')
#     client.force_login(guest_user)
#     response = client.get(url)
#     assert response.status_code == 403

#     # авторизован и есть права
#     url = reverse('project_app:project_own')
#     client.force_login(guest_user)
#     add_perm('project_owner', lambda _: True)
#     response = client.get(url)
#     assert response.status_code == 200

# @pytest.mark.django_db
# def test_guest_get_project_list_view(guest_user, client, project):

#     url = reverse('project_app:list')
#     response = client.get(url)

#     assert response.status_code == 200
#     assert project in response.context_data['projects']
#     assert len(response.context_data['projects']) == 1

# @pytest.mark.django_db
# def test_guest_get_project_detail_view(guest_user, client, project):

#     url = reverse('project_app:detail', kwargs={'project_id': project.id})
#     response = client.get(url)

#     assert response.status_code == 200
#     assert response.context['project'] == project

# @pytest.mark.django_db
# def test_auth_user_create_project(client, auth_user):
#     assert len(Project.objects.all()) == 0

#     data = {'title': 'New Project', 'description': 'New Description'}
#     url = reverse('project_app:create')
#     response = client.post(url, data)

#     assert response.status_code == 302
#     assert response.url == "/projects/1/"
#     project = Project.objects.get(title='New Project')
#     assert project.owner == auth_user
#     assert isinstance(project, Project)
#     assert project.title == 'New Project'
#     assert project.description == 'New Description'
#     assert len(Project.objects.all()) == 1

# @pytest.mark.django_db
# def test_guest_try_create_project(client, guest_user):
#     assert len(Project.objects.all()) == 0

#     url = reverse('project_app:create')
#     response = client.post(url)

#     assert response.status_code == 302
#     assert response.url == "/auth/login/?next=/projects/create/"
#     assert len(Project.objects.all()) == 0

# @pytest.mark.django_db
# def test_delete_project_by_owner(client, owner_user, project):
#     assert len(Project.objects.all()) == 1
#     project = Project.objects.first()
#     assert project.owner == owner_user

#     owner_user
#     url = reverse('project_app:delete', kwargs={'project_id': project.id})
#     response = client.post(url)

#     assert response.status_code == 302
#     assert len(Project.objects.all()) == 0

# @pytest.mark.django_db
# def test_delete_project_by_member(client, project, auth_user):
#     assert len(Project.objects.all()) == 1
#     project = Project.objects.first()
#     assert project.owner != auth_user

#     url = reverse('project_app:delete', kwargs={'project_id': project.id})
#     response = client.post(url)

#     assert response.status_code == 302
#     assert len(Project.objects.all()) == 1

# @pytest.mark.django_db
# def test_update_project_by_owner(client, owner_user, project):
#     assert len(Project.objects.all()) == 1
#     project = Project.objects.first()
#     assert project.title == 'Test Project'
#     assert project.description == 'Test Description'
#     assert project.owner == owner_user

#     url = reverse('project_app:update', kwargs={'project_id': project.id})
#     data = {'title': 'Updated Title', 'description': 'Updated Description'}
#     response = client.post(url, data)

#     assert response.status_code == 302
#     project.refresh_from_db()
#     assert len(Project.objects.all()) == 1
#     assert project.title == 'Updated Title'
#     assert project.description == 'Updated Description'

# # @pytest.mark.django_db
# # def test_include_member(project, user_second, role):
# #     membership = include_member(project, user_second, role)
# #     assert isinstance(membership, Membership)
# #     assert membership.project == project
# #     assert membership.user == user_second
# #     assert membership.role == role
# #     exclude_member(project, user_second)

# # @pytest.mark.django_db
# # def test_exclude_member(project, user_second, role):
# #     include_member(project, user_second, role)
# #     exclude_member(project, user_second)
# #     assert not Membership.objects.filter(project=project, user=user_second).exists()
