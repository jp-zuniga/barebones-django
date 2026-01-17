from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from api.exceptions import BadRequestError
from api.permissions import IsAdminOrReadOnly
from api.serializers.users import (
    ObtainTokenPairSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser, UserManager
    from rest_framework.permissions import BasePermission
    from rest_framework.request import Request

api_user = get_user_model()


class UserViewSet(ModelViewSet):
    permission_classes: ClassVar[list[type[BasePermission]]] = [IsAdminOrReadOnly]
    queryset: UserManager[AbstractUser] = api_user.objects.all().order_by("email")

    def get_serializer_class(  # type: ignore[reportIncompatibleMethodOverride]
        self,
    ) -> type[UserRegistrationSerializer | UserSerializer]:
        if self.action in ["create", "update", "partial_update"]:
            return UserRegistrationSerializer
        return UserSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:  # noqa: ANN002, ANN003, ARG002
        serializer: UserRegistrationSerializer | UserSerializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            user_data = UserSerializer(serializer.instance).data

            return Response(user_data, status=HTTP_201_CREATED, headers=headers)

        raise BadRequestError(str(serializer.errors))


class ObtainTokenPairView(TokenObtainPairView):
    serializer_class = ObtainTokenPairSerializer
