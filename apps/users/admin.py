from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "date_of_birth", "bio")
    search_fields = ("user__username", "bio")
    list_filter = ("date_of_birth",)


class UserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)


admin.site.register(User, UserAdmin)
