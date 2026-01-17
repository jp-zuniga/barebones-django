from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from django.db import OperationalError, connections
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.viewsets import ViewSet

if TYPE_CHECKING:
    from rest_framework.permissions import BasePermission
    from rest_framework.request import Request


class HealthViewSet(ViewSet):
    permission_classes: ClassVar[list[BasePermission]] = [AllowAny]  # type: ignore[reportAssignmentType]
    throttle_classes: ClassVar[list] = []

    def list(self, request: Request) -> Response:  # noqa: ARG002
        try:
            db_conn = connections["default"]
            db_conn.cursor()
        except OperationalError:
            return Response({"status": "db_error"}, status=HTTP_503_SERVICE_UNAVAILABLE)
        return Response({"status": "ok"}, status=HTTP_200_OK)
