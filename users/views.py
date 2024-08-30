from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import User, Payment
from users.permissions import IsSelfProfile
from users.serializers import (
    UserSerializer,
    PaymentsListSerializer,
    UserRetrieveSerializer,
    UserListSerializer,
    UserShortSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_object(self):
        obj = super().get_object()
        # Специально сохраняем pk получаемого объекта, для получения нужного сериализатора
        self.user_pk = obj.pk
        return obj

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        elif self.action == "retrieve":
            # Выбираем нужный сериализатор, исходя из совпадающего pk
            if self.request.user.pk == self.user_pk:
                return UserRetrieveSerializer
            else:
                return UserShortSerializer
        return UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [
                AllowAny,
            ]
        elif self.action in ("list", "retrieve"):
            self.permission_classes = [
                IsAuthenticated,
            ]
        else:
            self.permission_classes = [
                IsSelfProfile,
            ]
        return super().get_permissions()


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentsListSerializer
    queryset = Payment.objects.all()

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ("date",)
    filterset_fields = ("payment_course", "payment_lesson", "payment_method")
