from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import (
    UserCreateAPIView,
    UserProfileAPIView,
    UserDeleteAPIView,
    UserListAPIView,
    PaymentViewSet,
    CoursePaymentAPIView,
)
from users.apps import UsersConfig

app_name = UsersConfig.name  # Оставляем namespace (например, 'users')

router = DefaultRouter()
router.register(r"payments", PaymentViewSet)


@api_view(["GET"])
def payment_success(request):
    return Response({"status": "success"})


urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("profile/<int:pk>/", UserProfileAPIView.as_view(), name="profile-detail"),
    path("profile/", UserProfileAPIView.as_view(), name="profile-current"),
    path("profile/delete/", UserDeleteAPIView.as_view(), name="profile-delete"),
    path("", UserListAPIView.as_view(), name="users-list"),
    path(
        "courses/<int:course_id>/pay/",
        CoursePaymentAPIView.as_view(),
        name="course-pay",
    ),
    path(
        "payment/success/", payment_success, name="payment-success"
    ),  # Теперь обращение через users:payment-success
    path(
        "payment/cancel/",
        lambda request: Response({"status": "canceled"}),
        name="payment-cancel",
    ),
]

urlpatterns += router.urls
