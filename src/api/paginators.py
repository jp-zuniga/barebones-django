from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import urlparse

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.consts import MAX_PAGE_SIZE, MIN_PAGE_SIZE

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework.request import Request
    from rest_framework.views import APIView


class ApiPaginator(PageNumberPagination):
    max_page_size: int = MAX_PAGE_SIZE
    page_size: int = MIN_PAGE_SIZE
    page_size_query_param: str = "page_size"
    page_query_param: str = "page"

    def get_paginated_response(self, data: list) -> Response:
        return Response(
            {
                "elements": self.page.paginator.count,
                "next": self.simplify_link(self.get_next_link()),
                "previous": self.simplify_link(self.get_previous_link()),
                "current": self.page.number,
                "pages": self.page.paginator.num_pages,
                "results": data,
            }
        )

    def paginate_queryset(
        self,
        queryset: QuerySet,
        request: Request,
        view: APIView | None = None,
    ) -> list | None:
        page_size_param = request.query_params.get(self.page_size_query_param, "")

        if page_size_param == "0":
            return None

        return super().paginate_queryset(queryset, request, view)

    def simplify_link(self, link: str | None) -> str | None:
        if not link:
            return None

        return urlparse(link)._replace(scheme="", netloc="").geturl()
