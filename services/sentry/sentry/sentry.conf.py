"""
Sentry 26.x configuration for BeeCompose self-hosted deployment.

Docs: https://develop.sentry.dev/self-hosted/configuration/
"""

import os
from sentry.conf.server import *  # noqa: F401, F403

DATABASES = {
    "default": {
        "ENGINE": "sentry.db.postgres",
        "NAME": os.environ.get("POSTGRES_DB", "postgres"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": os.environ.get("POSTGRES_HOST", "pgbouncer"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 0,
        "AUTOCOMMIT": True,
        "OPTIONS": {
            "connect_timeout": 10,
        },
    }
}

# Prefer SENTRY_SYSTEM_SECRET_KEY; fall back to SENTRY_SECRET_KEY for compatibility
SENTRY_SYSTEM_SECRET_KEY = os.environ.get(
    "SENTRY_SYSTEM_SECRET_KEY",
    os.environ.get("SENTRY_SECRET_KEY", ""),
)

if not SENTRY_SYSTEM_SECRET_KEY or SENTRY_SYSTEM_SECRET_KEY.startswith("!!changeme!!"):
    raise RuntimeError(
        "SENTRY_SYSTEM_SECRET_KEY is not set or still uses the placeholder value. "
        "Generate a key with: docker compose run --rm web config generate-secret-key"
    )

SECRET_KEY = SENTRY_SYSTEM_SECRET_KEY

SENTRY_OPTIONS["system.secret-key"] = SENTRY_SYSTEM_SECRET_KEY

# Redis
SENTRY_OPTIONS["redis.clusters"] = {
    "default": {
        "hosts": {0: {"host": "redis", "password": "", "port": 6379, "db": 0}},
    }
}

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "memcached:11211",
        "TIMEOUT": 3600,
        "OPTIONS": {"ignore_exc": True},
    }
}

# Celery broker
CELERYBEAT_SCHEDULE_FILENAME = "/data/celerybeat-schedule"

# File store (filesystem, no S3/SeaweedFS required for errors-only profile)
SENTRY_OPTIONS["filestore.backend"] = "filesystem"
SENTRY_OPTIONS["filestore.options"] = {"location": "/data/files"}

# Mail — use SENTRY_MAIL_HOST env var to set the domain
mail_host = os.environ.get("SENTRY_MAIL_HOST", "localhost")
SENTRY_OPTIONS["mail.from"] = f"sentry@{mail_host}"
SENTRY_OPTIONS["mail.list-namespace"] = mail_host

# Always trust X-Forwarded-For / X-Forwarded-Proto from reverse proxy (Traefik)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Event retention
SENTRY_OPTIONS["system.event-retention-days"] = int(
    os.environ.get("SENTRY_EVENT_RETENTION_DAYS", 90)
)
