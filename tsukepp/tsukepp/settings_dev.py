"""
Django development settings for tsukepp project.
"""

from .settings_common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

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
