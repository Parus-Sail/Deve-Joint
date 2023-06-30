from django.contrib import admin

from .models import Membership, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    # list_filter = ('role',)
    # search_fields = ('title',)
    # search_fields = ('user__username', 'project__name', 'role__name')


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    ...
    # list_display = ('user', 'project', 'role')
    # Customize the displayed fields as needed
