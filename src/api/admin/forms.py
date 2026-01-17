from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from api.models.users import ApiUser

if TYPE_CHECKING:
    from collections.abc import Iterable


class ApiUserCreationForm(UserCreationForm):
    class Meta:
        model = ApiUser
        fields: Iterable[str] = (
            "email",
            "first_name",
            "last_name",
            "role",
        )


class ApiUserChangeForm(UserChangeForm):
    class Meta:
        model = ApiUser
        fields: str = "__all__"
