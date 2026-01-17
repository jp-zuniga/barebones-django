from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.admin import ModelAdmin

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework.request import Request

    from api.models.users import ApiUser


class SoftDeleteAdmin(ModelAdmin):
    def get_queryset(self, request: Request) -> QuerySet:  # noqa: ARG002 # type: ignore[incompatibleMethodOverride]
        return self.model.all_objects.get_queryset()

    def delete_model(self, request: Request, obj: ApiUser) -> None:  # noqa: ARG002 # type: ignore[incompatibleMethodOverride]
        obj.delete()
