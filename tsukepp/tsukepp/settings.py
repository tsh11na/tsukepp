"""Heroku用環境設定"""

from .settings_common import *
import dj_database_url
import django_heroku

DEBUG = False


ALLOWED_HOSTS = ['.herokuapp.com']

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

django_heroku.settings(locals())
