"""
Django development settings for tsukepp project.
"""

import socket  # For Django Debug Toolbar
from .settings_common import *

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

EMAILBACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_EMAIL_VERIFICATION = 'none'
