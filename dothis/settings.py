"""
Django settings for dothis project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
import sys

import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@xdi=2hzgxzv8m^vpsr2e6c=z3qghh%qhezuq0mdnx__fye(@q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'dothis',

    # External
    'import_export',
    'lettuce.django',
    'django_extensions',
    'foundation',
    'djrill',

    # Internal
    'volunteering',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dothis.urls'

WSGI_APPLICATION = 'dothis.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader')

# Lettuce settings
LETTUCE_USE_TEST_DATABASE = True
LETTUCE_APPS = (
    'volunteering',
)

# Parse database configuration from $DATABASE_URL
default_database_url = 'postgres://dothis:dothis@localhost:5432/dothis'
DATABASES = {
    'default': dj_database_url.config(default=default_database_url)
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

CSVIMPORT_MODELS = ['volunteering.Volunteer']


# Email config
SERVER_EMAIL = "office@nnls-masorti.org.uk"
MANDRILL_API_KEY = os.environ.get('MANDRILL_API_KEY', "fake_mandril_api_key")
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
FROM_ADDRESS = "New North London Security Team <security@nnls-masorti.org.uk>"
BCC_ADDRESSES = [FROM_ADDRESS, "a@heitler.com"]

# Djrill is a Mandril connection. It must override the admin.site early on.
from django.contrib import admin
from djrill import DjrillAdminSite
admin.site = DjrillAdminSite()

# Test overrides

if 'test' in sys.argv:
    PASSWORD_HASHERS = ('django_plainpasswordhasher.PlainPasswordHasher', )
