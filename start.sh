#!/usr/bin/env bash
set -e
python manage.py migrate --noinput
# Seed only when the listings table is empty (safe for first boot on Render)
python - <<'PY'
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from backend.app.models import Property
if Property.objects.count() == 0:
    from django.core.management import call_command
    call_command('seed_data')
    print('Seeded sample listings.')
else:
    print(f'Skipping seed ({Property.objects.count()} properties already exist).')
PY
exec python -m gunicorn backend.wsgi:application --bind 0.0.0.0:${PORT:-8000}
