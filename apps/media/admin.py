from django.contrib import admin
from .models import Multimedia


@admin.register(Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
    list_display = ("url", "type", "is_main_image", "is_content_image")
    search_fields = ("url", "type", "description")
    list_filter = ("type", "is_main_image", "is_content_image")
    ordering = ("-is_main_image", "type")
