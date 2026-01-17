from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import SAFE_METHODS, BasePermission

if TYPE_CHECKING:
    from rest_framework.request import Request
    from rest_framework.viewsets import ViewSet

    from api.models.users import ApiUser


class IsStaffOrReadOnly(BasePermission):
    def has_permission(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        request: Request,
        view: ViewSet,  # noqa: ARG002
    ) -> bool:
        user: ApiUser = request.user

        if not user or not user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return user.is_staff or user.is_superuser
