from django.contrib.auth import get_user_model
import rules
from rules import add_perm

from .models import Membership, Project

# from rules.permissions import DjangoPermission

User = get_user_model()


@rules.predicate()
def is_project_owner(user: User, project: Project):
    return project.owner == user


@rules.predicate
def is_project_member(user: User, project: Project):
    return user in project.members.all()


@rules.predicate
def is_not_project_member(user: User, project: Project):
    return user in project.members.all()


# Правило доступа для редактирования проекта
# add_perm('project_owner', DjangoPermission(is_project_owner))
add_perm('project_owner', is_project_owner)

# Правило доступа для удаления проекта
# add_perm('project_app.delete_project', DjangoPermission(lambda user, project: user == project.owner))

rules.add_rule("auth_user", rules.always_allow)
# rules.add_rule("project_owner", is_project_owner)
rules.add_rule("project_member", is_project_member)
rules.add_rule("project_not_member", is_not_project_member)

# rules.add_rule("project_member_change", is_project_owner)
# rules.add_rule("project_member_include", is_project_owner)
# rules.add_rule("project_member_exclude", is_project_owner)

# rules.add_rule("project_member_leave", is_project_member)
# rules.add_rule("project_member_invite", is_project_member | is_project_owner)
# # приглашение от участника (не требует подтвеждения от владельца проекта)
# rules.add_rule("project_member_approve_disapprove", is_not_project_member)
# rules.add_rule("project_member_application", is_not_project_member)
# заявление от желающего вступить (требует подтверждения от владельца проекта)