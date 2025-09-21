from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]
    list_filter = ["username", "email"]
    search_help_text = "username"
