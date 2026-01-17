from __future__ import annotations

from .admin import IsAdminOrReadOnly
from .staff import IsStaffOrReadOnly

__all__: list[str] = [
    "IsAdminOrReadOnly",
    "IsStaffOrReadOnly",
]
