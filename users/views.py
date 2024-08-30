from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions
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

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny,]
        else:
            pass
            # self.permission_classes = super().get_permissions()
        return [permission() for permission in self.permission_classes]


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentsListSerializer
    queryset = Payment.objects.all()

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ("date",)
    filterset_fields = ("payment_course", "payment_lesson", "payment_method")
