from django.contrib import admin
from .models import Multimedia


@admin.register(Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
    list_display = (
        "url",
        "type",
    )
    search_fields = ("url", "type", "description")
    list_filter = ("type",)
    ordering = ("type",)
