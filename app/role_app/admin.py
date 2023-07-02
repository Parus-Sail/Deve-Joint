from django.contrib import admin
from project_app.models import Membership

from .models import Role


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # Customize the displayed fields as needed
    inlines = [MembershipInline]