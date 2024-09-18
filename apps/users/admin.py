from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import User


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


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
