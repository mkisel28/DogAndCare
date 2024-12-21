from django.contrib import admin

from .models import DailyLog, Symptom, SymptomCategory


@admin.register(SymptomCategory)
class SymptomCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category"]
    list_filter = ["category"]
    search_fields = ["name"]


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ["id", "pet", "date", "created_at", "updated_at"]
    list_filter = ["date", "pet__owner"]
    search_fields = ["pet__name", "pet__owner__username"]
