"""
Django development settings for tsukepp project.
"""
import os
import socket  # For Django Debug Toolbar

from dotenv import load_dotenv

from .settings_common import *

# Load .env file
load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += [
    "debug_toolbar"
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
# https://code.djangoproject.com/ticket/33685
# Service for test may be implemented later:
# https://note.com/decoponia/n/nc75b36e2d1ee
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'service': 'DB',
            'passfile': '/workspaces/tsukepp/.pgpass',
        }
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'django_db',
    #     'HOST': 'localhost',
    #     'USER': config('DB_USER'),
    #     'PORT': config('DB_PORT'),
    #     'OPTIONS': {
    #         # 'service': 'DB',
    #         'passfile': '/workspaces/tsukepp/.pgpass',
    #     }
    # }
}

# Logging
# https://docs.djangoproject.com/en/4.2/topics/logging/
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "dev"
        }
    },
    "formatters": {
        "dev": {
            "format": "\t".join([
                "%(asctime)s",
                "[%(levelname)s]",
                "%(pathname)s(Line:%(lineno)d",
                "%(message)s"
            ])
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            # "propagate": True,
        },
        "tsuke": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "accounts": {
            "handlers": ["console"],
            "level": "DEBUG",
        }
    },
}

# Email
try:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
    DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'
    EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
except KeyError:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    ACCOUNT_EMAIL_VERIFICATION = 'none'

SECRET_KEY="secret_key"
