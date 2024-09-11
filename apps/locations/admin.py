from django.contrib import admin
from .models import Country, City, Language


class CityInline(admin.TabularInline):
    model = City
    extra = 1


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")
    list_filter = ("name", "code")
    inlines = [CityInline]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    search_fields = ("name", "country__name")
    list_filter = ("country",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")
    list_filter = ("name", "code")
