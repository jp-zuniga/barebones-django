from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from rest_framework.filters import SearchFilter

from api.exceptions import BadRequestError

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework.request import Request
    from rest_framework.views import APIView


class FuzzySearchFilter(SearchFilter):
    search_param: str = "search"
    field_param: str = "search_in"
    min_similarity: float = 0.1

    def filter_queryset(
        self,
        request: Request,
        queryset: QuerySet,
        view: APIView,
    ) -> QuerySet:
        target_field: str | None = request.query_params.get(self.field_param, None)
        search_term: str | None = request.query_params.get(self.search_param, None)

        if search_term is None:
            return queryset

        allowed_fields: list = getattr(view, "search_fields", [])

        if target_field is not None and target_field not in allowed_fields:
            model: str = (
                view.get_view_name()
                .removesuffix("List")
                .strip()
                .lower()
                .replace(" ", "-")
            )

            msg: str = f"`{model}` no tiene un atributo nombrado `{target_field}`."
            raise BadRequestError(msg)

        fields: list = allowed_fields if target_field is None else [target_field]

        if not fields:
            return queryset

        trigrams = [TrigramSimilarity(field, search_term) for field in fields]
        similarity_expr = Greatest(*trigrams) if len(trigrams) > 1 else trigrams[0]

        return (
            queryset.annotate(similarity=similarity_expr)
            .filter(similarity__gt=self.min_similarity)
            .order_by("-similarity")
        )
