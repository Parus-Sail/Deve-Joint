from django.contrib import admin

from .models import CV, BusyType, RelocationType


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ["owner", "title", "salary", "is_published"]
    search_fields = ["owner", "title", "salary", "is_published"]


@admin.register(BusyType)
class BusyTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(RelocationType)
class RelocationTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
