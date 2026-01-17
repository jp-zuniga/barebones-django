set quiet

[private]
default:
  just --list --list-heading $'  Recetas:\n' --list-prefix "    "

# ---------------------------------------------------------

# django check
check:
  uv run --frozen src/manage.py check

# ruff check --fix
fix:
  ruff check --fix --unsafe-fixes

# ruff format
fmt:
  ruff format

# ruff check
lint:
  ruff check --unsafe-fixes

# django makemigrations
mk-migrations:
  uv run --frozen src/manage.py makemigrations

# django migrate
migrate:
  uv run --frozen src/manage.py migrate

# django runserver
run:
  uv run --frozen src/manage.py runserver

# gunicorn server
serve:
  uv run --frozen gunicorn core.wsgi:application --chdir src --bind 0.0.0.0:8080

# pytest
test:
  uv run --frozen pytest

# pytest-ci
test-ci:
  uv run --frozen pytest --maxfail 1
