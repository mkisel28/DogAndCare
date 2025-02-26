from django.contrib import admin

from .models import Multimedia


@admin.register(Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
    list_display = ("id", "url", "type", "created_at")
    search_fields = ("url", "type", "description")
    list_filter = ("type", "created_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
