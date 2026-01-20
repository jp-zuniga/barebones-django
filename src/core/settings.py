"""
Global Django settings.
"""

from __future__ import annotations

from datetime import timedelta
from os import getenv
from pathlib import Path
from typing import TYPE_CHECKING

from dj_database_url import config as db_config
from dotenv import load_dotenv

if TYPE_CHECKING:
    from dj_database_url import DBConfig

load_dotenv()

# 1) ###################################################################################

BASE_DIR: Path = Path(__file__).resolve().parent.parent

if not getenv("DATABASE_URL"):
    msg: str = "Definir variable de entorno `DATABASE_URL`."
    raise RuntimeError(msg)
if not getenv("SECRET_KEY"):
    msg: str = "Definir variable de entorno `SECRET_KEY`."
    raise RuntimeError(msg)


DATABASE_URL: str = getenv("DATABASE_URL", "")
DEBUG: bool = getenv("DEBUG", "False").lower() == "true"
SECRET_KEY: str = getenv("SECRET_KEY", "")

# 2) ###################################################################################

APPEND_SLASH: bool = False
AUTH_USER_MODEL: str = "api.ApiUser"
ROOT_URLCONF: str = "core.urls"
WSGI_APPLICATION: str = "core.wsgi.application"
USE_X_FORWARDED_HOST: bool = True

# 3) ###################################################################################

LANGUAGE_CODE: str = "es"
TIME_ZONE: str = "America/Managua"
USE_I18N: bool = True
USE_TZ: bool = True

# 4) ###################################################################################

STATIC_URL: str = "/static/"
STATIC_ROOT: Path = BASE_DIR / "static"
STATICFILES_STORAGE: str = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# 5) ###################################################################################

INSTALLED_APPS: list[str] = [
    "api.apps.Api",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
]

MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# 6) ###################################################################################

ALLOWED_HOSTS: list[str] = [
    "localhost",
    "127.0.0.1",
    ".railway.app",
    ".up.railway.app",
]

CORS_ALLOW_CREDENTIALS: bool = not DEBUG
CORS_ALLOWED_ORIGINS: list[str] = [
    "http://localhost:8000",
]

CORS_ALLOWED_ORIGIN_REGEXES: list[str] = [
    r"^https://([a-z0-9-]+\.)?railway\.app$",
    r"^https://([a-z0-9-]+\.)?up\.railway\.app$",
]

CSRF_TRUSTED_ORIGINS: list[str] = [
    "http://localhost:8000",
    "https://*.railway.app",
    "https://*.up.railway.app",
]

# 7) ###################################################################################

DATABASES: dict[str, DBConfig] = {
    "default": db_config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# 8) ###################################################################################

REST_FRAMEWORK: dict[str, tuple[str] | str | list[str] | dict[str, str]] = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "api.paginators.ApiPaginator",
    "DEFAULT_PERMISSION_CLASSES": [
        "api.permissions.IsStaffOrReadOnly",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
    },
    "EXCEPTION_HANDLER": "api.exceptions.handler",
}

SIMPLE_JWT: dict[str, str | timedelta] = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "SIGNING_KEY": SECRET_KEY,
    "USER_ID_CLAIM": "user_id",
    "USER_ID_FIELD": "id",
}

# 9) ###################################################################################

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
]

TEMPLATES: list[dict[str, bool | str | list[str] | dict[str, list[str]]]] = [
    {
        "APP_DIRS": True,
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

#######################################################################################
