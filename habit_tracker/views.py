# -*- coding: utf-8 -*-
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from habit_tracker.models import HabitModel, RewordModel
from habit_tracker.pagination import MyPagination
from habit_tracker.serializers import HabitModelSerializer, RewordModelSerializer

from habit_tracker.validators import check_reword, is_pleasant_validator
from users.permissions import IsOwnerPermission, IsPublicPermission


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Получение объекта :model:habit_tracker.HabitModel.",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Создание объекта :model:habit_tracker.HabitModel.",
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Получение списка объектов :model:habit_tracker.HabitModel.",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Изменение объекта :model:habit_tracker.HabitModel.",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Частичное изменение объекта :model:habit_tracker.HabitModel.",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Удаление объекта :model:habit_tracker.HabitModel.",
    ),
)
@method_decorator(
    name="list_public_habits",
    decorator=swagger_auto_schema(
        operation_description="Получение списка общедоступных объектов :model:habit_tracker.HabitModel. "
        "Параметр is_public=True.",
    ),
)
class HabitViewSet(ModelViewSet):
    """ViewSet для операций над model: habit_tracker.HabitModel."""

    queryset = HabitModel.objects.all()
    serializer_class = HabitModelSerializer

    def list_public_habits(self, request):
        queryset = HabitModel.objects.filter(is_public=True)
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = HabitModelSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return HabitModel.objects.filter(
                is_public=True
            ) | HabitModel.objects.filter(user=user)
        else:
            return HabitModel.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        habit_id = int(self.kwargs.get("pk"))
        data = self.request.data
        pleasant_hab = data.get("pleasant_hab", False)
        reword = data.get("reword", False)
        is_pleasant_validator(
            pleasant_hab
        )  # проводим валидацию что привычка не является приятной
        check_reword(
            pleasant_hab, reword, habit_id
        )  # проводим валидацию что в изменяемой модели нет связанный вознаграждений и приятных привычек
        print(serializer)
        serializer.save()

    def get_permissions(self):

        if self.action == "create":
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = (IsOwnerPermission,)
        elif self.action == "retrieve":
            self.permission_classes = (IsOwnerPermission, IsPublicPermission)
        elif self.action == "list":
            self.permission_classes = (
                IsOwnerPermission,
                IsPublicPermission,
            )
        elif self.action == "list_public_habits":
            self.permission_classes = (AllowAny,)

        return super().get_permissions()


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Получение объекта :model:habit_tracker.RewordModel.",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Создание объекта :model:habit_tracker.RewordModel.",
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Получение списка объектов :model:habit_tracker.RewordModel.",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Изменение объекта :model:habit_tracker.RewordModel.",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Частичное изменение объекта :model:habit_tracker.RewordModel.",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Удаление объекта :model:habit_tracker.RewordModel.",
    ),
)
class RewordViewSet(ModelViewSet):
    """ViewSet для операций над model: habit_tracker.RewordModel."""

    queryset = RewordModel.objects.all()
    serializer_class = RewordModelSerializer
    permission_classes = (IsOwnerPermission, IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()
