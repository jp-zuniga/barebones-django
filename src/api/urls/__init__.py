from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from api.views.users import ObtainTokenPairView

from . import register, router, routes

if TYPE_CHECKING:
    from django.urls import URLPattern
    from django.urls.resolvers import URLResolver

__all__: list[str] = [
    "register",
    "router",
    "routes",
]

urlpatterns: list[URLPattern | URLResolver] = [
    path("auth/login", ObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/verify", TokenVerifyView.as_view(), name="token_verify"),
    path(
        route="",
        view=include(arg=register.register_routes().urls),
    ),
]
