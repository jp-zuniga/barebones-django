from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.models import UserManager

if TYPE_CHECKING:
    from .user import ApiUser


class ApiUserManager(UserManager):
    use_in_migrations = True

    def setup_user(
        self,
        email: str,
        password: str | None,
        **extra_fields,  # noqa: ANN003
    ) -> ApiUser:
        if not email:
            msg = "Debe proveer un correo electrónico."
            raise ValueError(msg)

        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_user(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        email: str,
        password: str | None = None,
        **extra_fields,  # noqa: ANN003
    ) -> ApiUser:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self.setup_user(email, password, **extra_fields)

    def create_superuser(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        email: str,
        password: str | None = None,
        **extra_fields,  # noqa: ANN003
    ) -> ApiUser:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            msg = "Superuser debe ser staff."
            raise ValueError(msg)
        if extra_fields.get("is_superuser") is not True:
            msg = "`is_superuser` debe ser `True`."
            raise ValueError(msg)

        return self.setup_user(email, password, **extra_fields)
