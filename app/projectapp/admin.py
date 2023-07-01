from django.contrib import admin
from roleapp.models import Role

from .models import Membership, Project


class RoleInline(admin.TabularInline):
    model = Role
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

    # list_filter = ('role',)
    # search_fields = ('title',)
    # search_fields = ('user__username', 'project__name', 'role__name')
    inlines = [RoleInline]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    ...
    # list_display = ('user', 'project', 'role')
    # Customize the displayed fields as needed
