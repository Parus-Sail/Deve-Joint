from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
import rules

from .models import Member, Membership, Owner, Project

User = get_user_model()
# anonymous_user = AnonymousUser()

# @rules.predicate
# def is_anonymous(user: User):
#     return user == anonymous_user


@rules.predicate
def is_project_owner(user: User, project: Project):
    return user == project.owner


@rules.predicate
def is_project_member(user: User, project: Project):
    return user in project.members.all()


@rules.predicate
def is_not_project_member(user: User, project: Project):
    return user in project.members.all()


rules.add_rule("view_list_project", rules.always_allow)
rules.add_rule("view_detail_project", rules.always_allow)
rules.add_rule("view_own_project", rules.is_project_owner)
rules.add_rule("create_project", rules.is_authenticated)
rules.add_rule("change_project", is_project_owner)
rules.add_rule("delete_project", is_project_owner)

rules.add_rule("view_project_member", rules.always_allow)
rules.add_rule("change_project_member", is_project_owner)

rules.add_rule("include", is_project_owner)
rules.add_rule("exclude", is_project_owner)

# приглашение от участника (не требует подтвеждения от владельца проекта)
rules.add_rule("invite", is_project_member | is_project_owner)
rules.add_rule("approve", is_not_project_member)
# заявление от желающего вступить (требует подтверждения от владельца проекта)
rules.add_rule("application", is_not_project_member)
rules.add_rule("accept_or_reject", is_project_owner)