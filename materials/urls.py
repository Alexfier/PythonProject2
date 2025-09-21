from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .apps import MaterialsConfig

router = DefaultRouter()

router.register("courses", views.CoursesViewSet, basename="courses")

app_name = MaterialsConfig.name

urlpatterns = [
    path("lessons/", views.LessonsListAPIView.as_view(), name="lessons"),
    path("lesson/create/", views.LessonsCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/<int:pk>/update/", views.LessonsUpdateAPIView.as_view(), name="lesson_update"),
    path("lesson/<int:pk>/destroy/", views.LessonsDestroyAPIView.as_view(), name="lesson_destroy"),
    path("lesson/<int:pk>/", views.LessonsRetrieveAPIView.as_view(), name="lesson"),
    path("courses/subscription/", views.SubscriptionAPIView.as_view(), name="subscription"),
] + router.urls
