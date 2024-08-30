from rest_framework import serializers

from users.models import User, Payment


class PaymentsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")


class UserRetrieveSerializer(serializers.ModelSerializer):
    payments = PaymentsListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"
