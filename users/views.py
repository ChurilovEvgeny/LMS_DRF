from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import User, Payment
from users.serializers import (
    UserSerializer,
    PaymentsListSerializer,
    UserRetrieveSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserRetrieveSerializer
        return UserSerializer


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentsListSerializer
    queryset = Payment.objects.all()

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ("date",)
    filterset_fields = ("payment_course", "payment_lesson", "payment_method")
