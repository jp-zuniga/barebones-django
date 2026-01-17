from __future__ import annotations

from django.db.models import Manager

from .querysets import SoftDeleteQuerySet


class SoftDeleteManager(Manager):
    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db).filter(
            deleted_at__isnull=True
        )

    def all_with_deleted(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db)

    def dead(self) -> SoftDeleteQuerySet:
        return self.all_with_deleted().dead()
