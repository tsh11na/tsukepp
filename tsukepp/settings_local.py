"""
Django development settings for tsukepp project.
"""
import os

from dotenv import load_dotenv

from .settings_common import *

# Load .env file
load_dotenv()

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# https://code.djangoproject.com/ticket/33685
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}

# Email
try:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
    EMAIL_HOST = os.environ['EMAIL_HOST']
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
except KeyError:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    ACCOUNT_EMAIL_VERIFICATION = 'none'

SECRET_KEY="secret_key"
