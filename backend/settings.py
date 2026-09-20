"""
Django settings for backend project.
"""

import os
from datetime import timedelta
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

BASE_DIR = Path(__file__).resolve().parent.parent


def _load_dotenv():
    """Load key=value from .env.local (file). `.env` is the local venv dir."""
    for name in ('.env.local', '.django.env'):
        env_path = BASE_DIR / name
        if not env_path.is_file():
            continue
        for raw in env_path.read_text().splitlines():
            line = raw.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)
        break


_load_dotenv()

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-9pf8#()oeiuk%8-dq4dh((smqklmuw8pvw7eq)2@h&ph!dv1=#',
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'true').lower() in ('1', 'true', 'yes')

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')
    if h.strip()
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'backend.app.apps.BackendAppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'backend' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


def _database_from_url(url: str):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    sslmode = (query.get('sslmode') or ['require'])[0]
    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': unquote(parsed.path.lstrip('/')),
        'USER': unquote(parsed.username or ''),
        'PASSWORD': unquote(parsed.password or ''),
        'HOST': parsed.hostname or '',
        'PORT': str(parsed.port or 5432),
        # Neon requires SSL. Omit channel_binding — it breaks some drivers.
        'OPTIONS': {'sslmode': sslmode},
    }


_database_url = os.environ.get('DATABASE_URL', '').strip()
if _database_url:
    DATABASES = {'default': _database_from_url(_database_url)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'backend' / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Frontend origins. Env CORS_ALLOWED_ORIGINS overrides this entire default list.
# If you set CORS_ALLOWED_ORIGINS on Render, include every frontend URL you use.
_cors_default = ','.join(
    [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
        'https://property-listing-frontend-iota.vercel.app',
    ]
)
_cors_origins = [
    o.strip()
    for o in os.environ.get('CORS_ALLOWED_ORIGINS', _cors_default).split(',')
    if o.strip()
]
CORS_ALLOWED_ORIGINS = _cors_origins
# Default: open in debug, respect CORS_ALLOWED_ORIGINS in production
CORS_ALLOW_ALL_ORIGINS = os.environ.get(
    'CORS_ALLOW_ALL_ORIGINS',
    'true' if DEBUG else 'false',
).lower() in ('1', 'true', 'yes')
CORS_ALLOW_CREDENTIALS = True

_csrf_default = ','.join(
    [
        'https://property-listing-frontend-iota.vercel.app',
        'https://poperty-listing-backend.onrender.com',
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ]
)
CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.environ.get('CSRF_TRUSTED_ORIGINS', _csrf_default).split(',')
    if o.strip()
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
