from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import CustomUser
from users.serializers import CustomUserSerializer


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Получение объекта :model:users.CustomUser.",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Создание объекта :model:users.CustomUser.",
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Получение списка объектов :model:users.CustomUser.",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Изменение объекта :model:users.CustomUser.",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Частичное изменение объекта :model:users.CustomUser.",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Удаление объектов :model:users.CustomUser.",
    ),
)
class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class MyTokenObtainPairView(TokenObtainPairView):
    """Аутентификация пользователя"""

    permission_classes = (AllowAny,)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email

        return token
