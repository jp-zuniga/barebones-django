from __future__ import annotations

from django.db.models import TextChoices


class ApiRoles(TextChoices):
    ADMIN = ("admin", "Administrador")
    STAFF = ("staff", "Personal")
