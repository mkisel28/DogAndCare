from django.contrib import admin
from .models import EmailVerificationCode


@admin.register(EmailVerificationCode)
class EmailVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "code", "created_at", "is_used")
    search_fields = ("user__username", "user__email", "code")
    list_filter = ("is_used", "created_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    raw_id_fields = ("user",)  

