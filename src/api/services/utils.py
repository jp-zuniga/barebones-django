from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING

from django.db import connection

from api.exceptions import NotFoundError
from api.models.base import BaseModel

if TYPE_CHECKING:
    from collections.abc import Generator

    from api.models.base import BaseModel


@contextmanager
def advisory_lock(lock_name: str) -> Generator:
    with connection.cursor() as cur:
        cur.execute("select pg_advisory_xact_lock(hashtext(%s))", [lock_name])

    try:
        yield
    finally:
        pass


def get_or_404(model: BaseModel, obj_id: str) -> BaseModel:
    try:
        return model.objects.get(id=obj_id)
    except model.DoesNotExist as e:
        raise NotFoundError(model.__name__, obj_id) from e
