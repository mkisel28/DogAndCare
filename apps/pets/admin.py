from django.contrib import admin
from apps.pets.models import Breed, Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "owner", "type", "breed", "sex", "is_neutered"]
    list_filter = ["type", "breed", "sex", "is_neutered"]
    search_fields = ["name", "owner__username"]
