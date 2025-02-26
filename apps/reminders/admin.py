from django.contrib import admin

from .models import Reminder, ReminderCategory, ReminderType

class ReminderTypeInline(admin.TabularInline):
    model = ReminderType
    extra = 1 

@admin.register(ReminderCategory)
class ReminderCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)
    ordering = ("name",)
    inlines = [ReminderTypeInline]


@admin.register(ReminderType)
class ReminderTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "is_active")
    search_fields = ("name", "category__name")
    list_filter = ("is_active", "category")
    ordering = ("category", "name")


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner",
        "reminder_type",
        "reminder_time",
        "is_recurring",
    )
    search_fields = ("title", "owner__username", "reminder_type__name")
    list_filter = ("is_recurring", "reminder_type", "owner")
    ordering = ("-reminder_time",)
    raw_id_fields = ("owner", "pets")
    date_hierarchy = "reminder_time"
