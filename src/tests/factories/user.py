from __future__ import annotations

from uuid import uuid4

from factory.declarations import LazyAttribute, LazyFunction
from factory.django import DjangoModelFactory
from faker import Faker
from rest_framework.authentication import get_user_model

faker = Faker("es")


class UserFactory(DjangoModelFactory):
    class Meta:  # type: ignore[incompatibleVariableOverride]
        model = get_user_model()
        skip_postgeneration_save = True

    id = LazyFunction(uuid4)

    email = LazyAttribute(lambda _: faker.unique.email().lower())
    first_name = LazyAttribute(lambda _: faker.first_name())
    last_name = LazyAttribute(lambda _: faker.last_name())

    is_active = True
    is_staff = False
    is_superuser = False
