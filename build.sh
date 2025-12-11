#!/usr/bin/env bash
set -o errexit

# Instala dependencias con Poetry (usa poetry.lock)
poetry install --no-interaction --no-ansi

# Ejecutar manage.py con poetry run para usar el entorno correcto
poetry run python manage.py collectstatic --no-input
poetry run python manage.py migrate --no-input
poetry run python manage.py cargar_demo