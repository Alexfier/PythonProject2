from django.contrib import admin

from habit_tracker.models import HabitModel, RewordModel


@admin.register(HabitModel)
class HabitAdmin(admin.ModelAdmin):
    list_display = ["name", "location", "id"]
    list_filter = ["name", "location"]
    search_help_text = "name"


@admin.register(RewordModel)
class RewordAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "id"]
    list_filter = ["name", "description"]
    search_help_text = ["name", "habit"]
