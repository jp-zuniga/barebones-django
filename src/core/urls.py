"""
Global URL configuration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.admin import site
from django.urls import include, re_path

if TYPE_CHECKING:
    from django.urls.resolvers import URLResolver

urlpatterns: list[URLResolver] = [
    re_path(r"^api/?", include("api.urls")),
    re_path(r"^admin/?", site.urls),
]
