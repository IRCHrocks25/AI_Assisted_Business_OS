#!/usr/bin/env bash
set -euo pipefail

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py ensure_superuser

PORT="${PORT:-8080}"
exec gunicorn myProject.wsgi:application --bind "0.0.0.0:${PORT}" --workers 2 --timeout 120
