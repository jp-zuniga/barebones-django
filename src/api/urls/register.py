from __future__ import annotations

from .router import Router
from .routes import ROUTES


def register_routes() -> Router:
    router = Router()

    for kebab_route, viewset in ROUTES:
        router.register(
            basename=kebab_route,
            prefix=kebab_route,
            viewset=viewset,
        )

    return router
