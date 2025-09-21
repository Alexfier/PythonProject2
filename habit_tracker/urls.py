from rest_framework.routers import SimpleRouter
from habit_tracker.apps import HabitTrackerConfig
from django.urls import path
from habit_tracker.views import HabitViewSet, RewordViewSet

app_name = HabitTrackerConfig.name

router = SimpleRouter()
router.register("habits", HabitViewSet)
router.register("rewords", RewordViewSet)

urlpatterns = [
    path("habits/public/", HabitViewSet.as_view({"get": "list_public_habits"}))
] + router.urls
