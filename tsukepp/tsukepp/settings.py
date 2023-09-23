"""Heroku用環境設定"""

from .settings_common import *
import dj_database_url
import django_heroku

DEBUG = False

django_heroku.settings(locals())

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

STATIC_ROOT = BASE_DIR / "staticfiles"

# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

