from rest_framework.serializers import ModelSerializer

from .models import Payments, User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PaymentsModelSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"
