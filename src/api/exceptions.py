from __future__ import annotations

from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import exception_handler as drf_handler


class DomainError(Exception):
    pass


class BadRequestError(DomainError):
    pass


class ConflictError(DomainError):
    pass


class UnauthorizedError(DomainError):
    pass


class NotFoundError(DomainError):
    def __init__(self, model: str, obj_id: str) -> None:
        super().__init__(f"{model} con id={obj_id} no existe.")


def handler(exc: Exception, context: dict) -> Response | None:  # noqa: PLR0911
    resp = drf_handler(exc, context)

    if resp is not None:
        return resp

    if isinstance(exc, DomainError):
        data = {"detail": str(exc)}

        if isinstance(exc, UnauthorizedError):
            return Response(exc, HTTP_401_UNAUTHORIZED)
        if isinstance(exc, NotFoundError):
            return Response(data, status=HTTP_404_NOT_FOUND)
        if isinstance(exc, ConflictError):
            return Response(data, status=HTTP_409_CONFLICT)

        return Response(data, status=HTTP_400_BAD_REQUEST)

    if not settings.DEBUG:
        return Response(
            {"detail": "Error interno del servidor."},
            status=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return None
