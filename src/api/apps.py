"""
Django app configuration.
"""

from __future__ import annotations

from django.apps import AppConfig


class Api(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    label = "api"
    name = "api"

    def ready(self) -> None:
        import api.models
