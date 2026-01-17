from __future__ import annotations

from uuid import uuid4

from django.db.models import BooleanField, DateTimeField, Manager, Model, UUIDField
from django.utils import timezone

from .managers import SoftDeleteManager


class BaseModel(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)

    is_active = BooleanField(default=True, editable=False)
    deleted_at = DateTimeField(
        blank=True,
        editable=False,
        db_index=True,
        null=True,
    )

    all_objects = Manager()
    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def delete(
        self,
        using=None,  # noqa: ANN001, ARG002
        keep_parents=False,  # noqa: ANN001, ARG002, FBT002
    ) -> tuple[int, dict[str, int]]:
        self.is_active = False
        self.deleted_at = timezone.now()

        self.save(update_fields=["is_active", "deleted_at"])

        return (1, {self._meta.label: 1})

    def hard_delete(
        self,
        using=None,  # noqa: ANN001
        keep_parents=False,  # noqa: ANN001, FBT002
    ) -> tuple[int, dict[str, int]]:
        return super().delete(using=using, keep_parents=keep_parents)
