from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import QuerySet
from django.utils import timezone

if TYPE_CHECKING:
    from typing import Self


class SoftDeleteQuerySet(QuerySet):
    def delete(self) -> int:  # type: ignore[reportIncompatibleMethodOverride]
        return self.update(deleted_at=timezone.now(), is_active=False)

    def hard_delete(self) -> tuple[int, dict[str, int]]:
        return super().delete()

    def alive(self) -> Self:
        return self.filter(deleted_at__isnull=True)

    def dead(self) -> Self:
        return self.filter(deleted_at__isnull=False)
