from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

if TYPE_CHECKING:
    from collections.abc import Iterable

    from rest_framework_simplejwt.tokens import Token

    from api.models.users import ApiUser

api_user = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields: Iterable[str] = (
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_active",
            "last_login",
            "date_joined",
        )

        model = api_user
        read_only_fields: Iterable[str] = fields


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
        )

        model = api_user

    def create(self, validated_data: dict) -> ApiUser:
        return api_user.objects.create_user(**validated_data)  # type: ignore[reportReturnType]


class ObtainTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: ApiUser) -> Token:  # type: ignore[reportIncompatibleMethodOverride]
        token = super().get_token(user)

        token["email"] = user.email
        token["role"] = user.role

        return token

    def validate(self, attrs: dict) -> dict:
        data: dict = super().validate(attrs)

        data["user"] = {
            "id": str(self.user.id),  # type: ignore[reportOptionalMemberAccess]
            "email": self.user.email,  # type: ignore[reportOptionalMemberAccess]
            "first_name": self.user.first_name,  # type: ignore[reportOptionalMemberAccess]
            "last_name": self.user.last_name,  # type: ignore[reportOptionalMemberAccess]
            "role": self.user.role,  # type: ignore[reportOptionalMemberAccess]
        }

        return data
