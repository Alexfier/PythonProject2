from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt import views

from . import services
from .models import Payments, User
from .serializers import PaymentsModelSerializer, UserModelSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(self.request.data.get("password"))
        user.save()


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsModelSerializer
    queryset = Payments.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ("date_payments",)
    filterset_fields = ("paid_lesson", "paid_course", "payment_method")

    def perform_create(self, serializer):
        payment = serializer.save()
        price_id = services.create_price(product=services.create_product(), amount=payment.payment_amount)
        link = services.create_session(price_id)
        payment.payment_link = link


class UserTokenObtainPairView(views.TokenObtainPairView):
    permission_classes = [AllowAny]


class UserTokenRefreshView(views.TokenRefreshView):
    permission_classes = [AllowAny]
