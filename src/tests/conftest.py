from __future__ import annotations

from datetime import UTC, datetime, timedelta
from os import environ
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from typing import TYPE_CHECKING

from django.conf import settings
from faker import Faker
from freezegun import freeze_time
from pytest import fixture, mark
from rest_framework.test import APIClient

from api.models.users import ApiUser

from .factories import UserFactory

if TYPE_CHECKING:
    from collections.abc import Generator

    from pytest import (
        Config as PytestConfig,
        Item as ConfigItem,
    )


TestClient = tuple[APIClient, ApiUser]


def pytest_configure() -> None:
    environ.setdefault("SKIP_SEED_MIGRATION", "True")


def pytest_collection_modifyitems(
    config: PytestConfig,  # noqa: ARG001
    items: list[ConfigItem],
) -> None:
    for item in items:
        parts: list[str] = [s.lower() for s in Path(str(item.fspath)).parts]

        if "unit" in parts:
            item.add_marker(mark.unit)

        item.add_marker(mark.django_db(transaction=False))


# --------------------------------------------------------------------------------------


@fixture(autouse=True)
def clean_media_root() -> Generator:
    root: str | None = getattr(settings, "MEDIA_ROOT", None)
    yield

    if root and Path(root).is_dir():
        rmtree(root, ignore_errors=True)
        Path(root).mkdir(parents=True, exist_ok=True)


@fixture(scope="session")
def faker() -> Faker:
    return Faker("es")


@fixture
def frozen_time() -> Generator:
    year: int = datetime.now(tz=UTC).year

    with freeze_time(f"{year}-01-01 12:00:00"):
        yield


@fixture(autouse=True, scope="session")
def test_settings() -> None:
    settings.ALLOWED_HOSTS = ["*"]
    settings.DEBUG = False
    settings.MEDIA_ROOT = Path(mkdtemp())
    settings.STATIC_ROOT = Path(mkdtemp())
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

    if isinstance(getattr(settings, "SIMPLE_JWT", None), dict):
        settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(minutes=5)

    settings.STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )


# --------------------------------------------------------------------------------------


def force_authenticate(client: APIClient, **kwargs: bool) -> TestClient:
    user: ApiUser = UserFactory(**kwargs)

    user.set_password("secret1234")
    user.save(update_fields=["password"])

    client.force_authenticate(user=user)

    return client, user


@fixture
def client() -> APIClient:
    return APIClient()


@fixture
def auth_client() -> TestClient:
    return force_authenticate(APIClient())


@fixture
def staff_client() -> TestClient:
    return force_authenticate(APIClient(), is_staff=True)


@fixture
def admin_client() -> TestClient:
    return force_authenticate(APIClient(), is_staff=True, is_superuser=True)
