# This file is just Python, with a touch of Django which means
# you can inherit and tweak settings to your hearts content.
#
# NOTE: This file is provided as a reference/customization template.
# On first run, the named volume `sentry_config` is populated from the
# image's default /etc/sentry/. Copy this file into the volume to override:
#   docker cp sentry.conf.py sentry:/etc/sentry/sentry.conf.py
#
# Supported environment variables (passed via sentry.env):
#  SENTRY_SYSTEM_SECRET_KEY  - Secret key (preferred, 25.x+)
#  SENTRY_SECRET_KEY         - Secret key (legacy fallback)
#  SENTRY_EVENT_RETENTION_DAYS - Days to retain events (default: 90)
#  SENTRY_POSTGRES_HOST
#  SENTRY_POSTGRES_PORT
#  SENTRY_DB_NAME
#  SENTRY_DB_USER
#  SENTRY_DB_PASSWORD
#  SENTRY_REDIS_HOST
#  SENTRY_REDIS_PASSWORD
#  SENTRY_REDIS_PORT
#  SENTRY_REDIS_DB
#  SENTRY_MEMCACHED_HOST
#  SENTRY_MEMCACHED_PORT
#  SENTRY_SERVER_EMAIL
#  SENTRY_EMAIL_HOST
#  SENTRY_EMAIL_PORT
#  SENTRY_EMAIL_USER
#  SENTRY_EMAIL_PASSWORD
#  SENTRY_EMAIL_USE_TLS
#  SENTRY_ENABLE_EMAIL_REPLIES
#  SENTRY_SMTP_HOSTNAME
#  SENTRY_MAILGUN_API_KEY
#  GITHUB_APP_ID
#  GITHUB_API_SECRET
#  BITBUCKET_CONSUMER_KEY
#  BITBUCKET_CONSUMER_SECRET
from sentry.conf.server import *  # NOQA

import os
import os.path

CONF_ROOT = os.path.dirname(__file__)

###########
# General #
###########

SENTRY_SINGLE_ORGANIZATION = True

SENTRY_OPTIONS["system.event-retention-days"] = int(
    env("SENTRY_EVENT_RETENTION_DAYS", "90")
)

################
# Secret Key   #
################

# SENTRY_SYSTEM_SECRET_KEY is preferred in 25.x+; SENTRY_SECRET_KEY is the legacy name.
secret_key = env("SENTRY_SYSTEM_SECRET_KEY") or env("SENTRY_SECRET_KEY")
if not secret_key:
    raise Exception(
        "Error: SENTRY_SYSTEM_SECRET_KEY is undefined. "
        "Generate one with: docker exec -it sentry sentry config generate-secret-key"
    )

if "SENTRY_RUNNING_UWSGI" not in os.environ and len(secret_key) < 32:
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!                    CAUTION                       !!")
    print("!! Your SENTRY_SYSTEM_SECRET_KEY is potentially     !!")
    print("!! insecure. Recommend at least 32 characters.      !!")
    print("!! Regenerate: sentry config generate-secret-key    !!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

SENTRY_OPTIONS["system.secret-key"] = secret_key

############
# Database #
############

DATABASES = {
    "default": {
        "ENGINE": "sentry.db.postgres",
        "NAME": env("SENTRY_DB_NAME") or "sentry",
        "USER": env("SENTRY_DB_USER") or "postgres",
        "PASSWORD": env("SENTRY_DB_PASSWORD") or "",
        "HOST": env("SENTRY_POSTGRES_HOST") or "postgres",
        "PORT": env("SENTRY_POSTGRES_PORT") or "",
    }
}

#########
# Redis #
#########

redis_host = env("SENTRY_REDIS_HOST") or "redis"
redis_password = env("SENTRY_REDIS_PASSWORD") or ""
redis_port = env("SENTRY_REDIS_PORT") or "6379"
redis_db = env("SENTRY_REDIS_DB") or "0"

SENTRY_OPTIONS["redis.clusters"] = {
    "default": {
        "hosts": {
            0: {
                "host": redis_host,
                "password": redis_password,
                "port": redis_port,
                "db": redis_db,
            }
        }
    }
}

#########
# Cache #
#########

memcached_host = env("SENTRY_MEMCACHED_HOST") or "memcached"
memcached_port = env("SENTRY_MEMCACHED_PORT") or "11211"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": ["{0}:{1}".format(memcached_host, memcached_port)],
        "TIMEOUT": 3600,
        "OPTIONS": {"ignore_exc": True},
    }
}

SENTRY_CACHE = "sentry.cache.redis.RedisCache"

#########
# Queue #
#########

BROKER_URL = "redis://:{password}@{host}:{port}/{db}".format(
    password=redis_password,
    host=redis_host,
    port=redis_port,
    db=redis_db,
)

################
# File storage #
################

SENTRY_OPTIONS["filestore.backend"] = "filesystem"
SENTRY_OPTIONS["filestore.options"] = {
    "location": env("SENTRY_FILESTORE_DIR") or "/var/lib/sentry/files",
}

##############
# Web Server #
##############

# Behind a reverse SSL proxy (Traefik), enable X-Forwarded-Proto support.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

SENTRY_WEB_HOST = "0.0.0.0"
SENTRY_WEB_PORT = 9000

###############
# Mail Server #
###############

email_host = env("SENTRY_EMAIL_HOST")
if email_host:
    SENTRY_OPTIONS["mail.backend"] = "smtp"
    SENTRY_OPTIONS["mail.host"] = email_host
    SENTRY_OPTIONS["mail.password"] = env("SENTRY_EMAIL_PASSWORD") or ""
    SENTRY_OPTIONS["mail.username"] = env("SENTRY_EMAIL_USER") or ""
    SENTRY_OPTIONS["mail.port"] = int(env("SENTRY_EMAIL_PORT") or 25)
    SENTRY_OPTIONS["mail.use-tls"] = env("SENTRY_EMAIL_USE_TLS", False)
else:
    SENTRY_OPTIONS["mail.backend"] = "dummy"

SENTRY_OPTIONS["mail.from"] = env("SENTRY_SERVER_EMAIL") or "root@localhost"

mailgun_key = env("SENTRY_MAILGUN_API_KEY") or ""
SENTRY_OPTIONS["mail.mailgun-api-key"] = mailgun_key

if mailgun_key:
    SENTRY_OPTIONS["mail.enable-replies"] = True
else:
    SENTRY_OPTIONS["mail.enable-replies"] = env("SENTRY_ENABLE_EMAIL_REPLIES", False)

if SENTRY_OPTIONS["mail.enable-replies"]:
    SENTRY_OPTIONS["mail.reply-hostname"] = env("SENTRY_SMTP_HOSTNAME") or ""

##################
# Integrations   #
##################

if "GITHUB_APP_ID" in os.environ:
    GITHUB_EXTENDED_PERMISSIONS = ["repo"]
    GITHUB_APP_ID = env("GITHUB_APP_ID")
    GITHUB_API_SECRET = env("GITHUB_API_SECRET")

if "BITBUCKET_CONSUMER_KEY" in os.environ:
    BITBUCKET_CONSUMER_KEY = env("BITBUCKET_CONSUMER_KEY")
    BITBUCKET_CONSUMER_SECRET = env("BITBUCKET_CONSUMER_SECRET")

SENTRY_FEATURES["auth:register"] = False
