"""Heroku用環境設定"""

import dj_database_url
import django_heroku

from .settings_common import *

DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

DATABASES = {
# https://code.djangoproject.com/ticket/33685
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'name',
        'HOST': 'host',
        'USER': 'user',
        'PORT': '',
        'PASSWORD': '',
    }
}

django_heroku.settings(locals())
