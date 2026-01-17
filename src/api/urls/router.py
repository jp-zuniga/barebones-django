from __future__ import annotations

from rest_framework.routers import DefaultRouter


class Router(DefaultRouter):
    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)

        self.trailing_slash = r"/?"
