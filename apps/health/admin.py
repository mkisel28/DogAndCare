from django.contrib import admin
from apps.pets.models import Breed, Pet
from .models import SymptomCategory, Symptom, DailyLog


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
