from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from api.models.users import ApiUser

from .forms import ApiUserChangeForm, ApiUserCreationForm

if TYPE_CHECKING:
    from django.contrib.admin.options import _FieldsetSpec as FieldSet
    from django.db.models import QuerySet
    from rest_framework.request import Request

from .delete import SoftDeleteAdmin


@register(ApiUser)
class ApiUserAdmin(UserAdmin, SoftDeleteAdmin):
    form: type = ApiUserChangeForm
    add_form: type = ApiUserCreationForm

    add_fieldsets: FieldSet = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "role",
                ),
            },
        ),
    )

    fieldsets: FieldSet = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined", "deleted_at")}),
    )

    list_display: ClassVar[list[str]] = [  # type: ignore[reportIncompatibleMethodOverride]
        "email",
        "first_name",
        "last_name",
        "role",
        "is_staff",
        "is_active",
    ]

    ordering: ClassVar[list[str]] = ["email"]  # type: ignore[reportIncompatibleMethodOverride]
    readonly_fields: ClassVar[list[str]] = [  # type: ignore[reportIncompatibleMethodOverride]
        "is_active",
        "deleted_at",
        "last_login",
        "date_joined",
    ]

    search_fields: ClassVar[list[str]] = ["email", "first_name", "last_name"]  # type: ignore[reportIncompatibleMethodOverride]

    def get_queryset(self, request: Request) -> QuerySet:  # noqa: ARG002 # type: ignore[incompatibleMethodOverride]
        return self.model.all_objects.get_queryset()
