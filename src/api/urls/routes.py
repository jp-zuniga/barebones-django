from __future__ import annotations

from api.views.health import HealthViewSet
from api.views.users import UserViewSet

ROUTES: list[tuple[str, type]] = [
    ("health", HealthViewSet),
    ("users", UserViewSet),
]
