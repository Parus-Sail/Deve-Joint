from project_app.models import Membership, Owner, Project
from project_app.views.mixins import (  # ProjectMixin,; OwnProjectMixin,; OwnProjectEditMixin,; WithAllMembershipMixin,; WithActiveMembershipMixin,
    OwnerEditMixin, OwnerMixin,
)
import pytest

# =================================================================

# ============================================= MIXINS =============================================


def test_owner_mixin_get_queryset(owner_mixin):
    queryset = owner_mixin.get_queryset()
    assert queryset is not None
    # Add assertions for the expected behavior of get_queryset()


def test_owner_mixin_test_func(owner_mixin):
    owner_mixin.kwargs = {'pk': 1}
    assert owner_mixin.test_func() is True
    # Add assertions for the expected behavior of test_func()


def test_owner_edit_mixin_form_valid(owner_edit_mixin):
    form = object()  # Replace with an actual form instance
    with pytest.raises(AttributeError):
        owner_edit_mixin.form_valid(form)
    # Add assertions for the expected behavior of form_valid()


def test_project_mixin(project_mixin):
    assert project_mixin.model == Project
    assert project_mixin.pk_url_kwarg == 'project_id'
    # Add assertions for any additional expected behavior of the mixin


def test_own_project_mixin(own_project_mixin):
    assert isinstance(own_project_mixin, OwnerMixin)
    assert isinstance(own_project_mixin, ProjectMixin)
    # Add assertions for any additional expected behavior of the mixin


def test_own_project_edit_mixin(own_project_edit_mixin):
    assert isinstance(own_project_edit_mixin, OwnProjectMixin)
    assert isinstance(own_project_edit_mixin, OwnerEditMixin)
    # Add assertions for any additional expected behavior of the mixin


def test_with_all_membership_mixin_get_queryset(with_all_membership_mixin):
    queryset = with_all_membership_mixin.get_queryset()
    assert queryset is not None
    # Add assertions for the expected behavior of get_queryset()


def test_with_active_membership_mixin_get_queryset(with_active_membership_mixin):
    queryset = with_active_membership_mixin.get_queryset()
    assert queryset is not None
    # Add assertions for the expected behavior of get_queryset()


# ============================================= VIEWS =============================================


def test_project_list_view(client):
    response = client.get('/project/list/')
    assert response.status_code == 200
    # Add assertions for the expected behavior of the view


def test_project_detail_view(client, project):
    response = client.get(f'/project/detail/{project.pk}/')
    assert response.status_code == 200
    # Add assertions for the expected behavior of the view


# Add tests for the remaining views in project_views.py

# Run the tests using pytest
