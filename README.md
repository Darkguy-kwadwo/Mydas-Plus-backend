# Mydas Plus — Backend (Django)

Self-contained Django API + admin for Mydas Plus.

## Run locally

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser   # optional
python manage.py runserver 0.0.0.0:8000
```

## Layout

```
backend/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── media/                 # uploaded images
└── backend/               # project package
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    ├── asgi.py
    ├── app/               # listings models, API, admin
    ├── templates/
    └── static/
```

## Production notes

- Default `CORS_ALLOWED_ORIGINS` includes localhost + `https://property-listing-frontend-iota.vercel.app`
- If you set `CORS_ALLOWED_ORIGINS` on Render, **include the Vercel URL** — the env var replaces the default list
- Start command: `bash start.sh` (migrate + seed-if-empty + gunicorn)
- Prefer Postgres instead of SQLite for production
