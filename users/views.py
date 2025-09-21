from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import CustomsUser, Payments
from users.serializers import CustomsUserSerializer, PaymentsSerializer
from users.services import (
    creating_product_stripe,
    creating_price_stripe,
    creating_session_stripe,
)


class UserCreateAPIView(CreateAPIView):
    """CRUD для регистрации пользователя"""

    serializer_class = CustomsUserSerializer
    queryset = CustomsUser.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentsViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "payment_method",
    )
    ordering_fields = ("payment_date",)


class PaymentCreateAPIView(CreateAPIView):
    """Оплата курса через страйп"""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_id = creating_product_stripe(payment)
        price_id = creating_price_stripe(product_id, payment)
        session_id, session_url = creating_session_stripe(price_id)
        payment.session_id = session_id
        payment.link = session_url
        payment.save()


class CustomsUserViewSet(ModelViewSet):
    """Пользовательское вью"""

    queryset = CustomsUser.objects.all()
    serializer_class = CustomsUserSerializer
