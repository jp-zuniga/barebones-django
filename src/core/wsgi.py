"""
WSGI configuration.
"""

from __future__ import annotations

from os import environ
from typing import TYPE_CHECKING

from django.core.wsgi import get_wsgi_application

if TYPE_CHECKING:
    from django.core.handlers.wsgi import WSGIHandler

environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application: WSGIHandler = get_wsgi_application()
