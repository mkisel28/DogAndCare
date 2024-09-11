from django.contrib import admin
from .models import (
    UserProfile,
    AnonymousUser,
    UserActivity,
    UserReaction,
    UserReactionType,
)
from django.contrib.auth.models import User


class UserActivityInline(admin.TabularInline):
    model = UserActivity
    extra = 1


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(UserReaction)
class UserReactionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "news_article",
        "story_article",
        "reaction_type",
        "timestamp",
    )
    search_fields = ("user__username",)
    list_filter = ("reaction_type", "timestamp")


@admin.register(UserReactionType)
class UserReactionTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "is_source_admin", "date_of_birth", "bio")
    search_fields = ("user__username", "bio")
    list_filter = ("is_source_admin", "date_of_birth")


@admin.register(AnonymousUser)
class AnonymousUserAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "last_activity")
    search_fields = ("id",)
    list_filter = ("created_at", "last_activity")
    inlines = [UserActivityInline]


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "anon_user",
        "news_article",
        "story_article",
        "action",
        "timestamp",
        "path",
        "device_type",
    )
    search_fields = (
        "user__username",
        "anon_user__id",
        "news_article__title",
        "story_article__title",
    )
    list_filter = ("action", "timestamp")


# Define a new User admin
class UserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
