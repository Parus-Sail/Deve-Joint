from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from MainPageApp import models as mainpage_models


@admin.register(mainpage_models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "created", "deleted"]
    search_fields = ["title", "preamble", "body"]
    actions = ["mark_deleted"]

    def mark_deleted(self, request, queryset):
        queryset.update(deleted=True)

    mark_deleted.short_description = _("Mark deleted")