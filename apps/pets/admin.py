from django.contrib import admin

from apps.pets.models import Breed, Pet, Temperament


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "size",
        "lifespan",
        "min_weight",
        "max_weight",
        "sheds",
    )
    search_fields = ("name", "size")
    list_filter = ("size", "sheds")
    ordering = ("name",)


@admin.register(Temperament)
class TemperamentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "owner", "type", "breed", "sex", "is_neutered"]
    list_filter = ["type", "breed", "sex", "is_neutered"]
    search_fields = ["name", "owner__username"]
