from __future__ import annotations

from unittest.mock import Mock

from api.permissions import IsAdminOrReadOnly, IsStaffOrReadOnly


def test_is_admin_or_read_only() -> None:
    perm = IsAdminOrReadOnly()
    request = Mock()
    view = Mock()

    request.user.is_authenticated = False

    assert not perm.has_permission(request, view)

    request.user.is_authenticated = True
    request.user.is_superuser = False
    request.method = "POST"

    assert not perm.has_permission(request, view)

    request.user.is_superuser = True

    assert perm.has_permission(request, view)

    request.user.is_superuser = False
    request.method = "GET"

    assert perm.has_permission(request, view)


def test_is_staff_or_read_only() -> None:
    perm = IsStaffOrReadOnly()
    request = Mock()
    view = Mock()

    request.user.is_authenticated = False

    assert not perm.has_permission(request, view)

    request.user.is_authenticated = True
    request.user.is_staff = False
    request.user.is_superuser = False
    request.method = "POST"

    assert not perm.has_permission(request, view)

    request.user.is_staff = True

    assert perm.has_permission(request, view)

    request.user.is_staff = False
    request.method = "GET"

    assert perm.has_permission(request, view)
