from __future__ import annotations

from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import GinIndex
from django.db.models import CharField, EmailField, Index, Q, UniqueConstraint
from django.db.models.functions import Lower

from api.models.base import BaseModel

from .manager import ApiUserManager
from .roles import ApiRoles


class ApiUser(BaseModel, AbstractUser):
    email = EmailField(db_index=True, unique=True)
    role = CharField(choices=ApiRoles.choices)
    username = None

    objects = ApiUserManager()

    REQUIRED_FIELDS: ClassVar[list[str]] = [  # type: ignore[incompatibleVariableOverride]
        "first_name",
        "last_name",
    ]

    USERNAME_FIELD = "email"

    class Meta(BaseModel.Meta):
        constraints: ClassVar[list[UniqueConstraint]] = [
            UniqueConstraint(
                Lower("email"),
                condition=Q(deleted_at__isnull=True),
                name="unq_user_email",
            ),
        ]

        ordering: ClassVar[list[str]] = ["email"]
        indexes: ClassVar[list[Index]] = [
            GinIndex(
                fields=["email"],
                opclasses=["gin_trgm_ops"],
                name="gin_user_email",
            ),
        ]

    def __str__(self) -> str:
        return self.email

    @property
    def permission(self) -> str:
        if getattr(self, "is_superuser", False):
            return "admin"
        if getattr(self, "is_staff", False):
            return "staff"
        return "user"
