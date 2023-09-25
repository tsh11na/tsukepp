"""
Django development settings for tsukepp project.
"""

import os
import socket  # For Django Debug Toolbar

from .settings_common import *

# from decouple import config


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
# https://code.djangoproject.com/ticket/33685

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_NAME"),
        # 'NAME': "postgres",
        'HOST': os.environ.get("POSTGRES_HOST", "db"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'PORT': os.environ.get("POSTGRES_PORT", 5432),
    }
}

EMAILBACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_EMAIL_VERIFICATION = 'none'

SECRET_KEY="secret_key"
