from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
from users.views import CustomUserViewSet, MyTokenObtainPairView
from django.urls import path

app_name = UsersConfig.name

router = SimpleRouter()
router.register("users", CustomUserViewSet)

urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name="login"),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny)),
        name="token_refresh",
    ),
] + router.urls
