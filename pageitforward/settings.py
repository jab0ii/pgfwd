"""
Django settings for pageitforward project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+g$i%iq$lkzvy*lyi4ox@megrvu(vf8dg8r05*v+jhof&#ijg2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Foreman doesn't pass stderr output back to us, so we have to override
# logging for Django and gunicorn to see the logs.
if DEBUG:
    LOGGING = {
        'version': 1,
        'formatters':
        {
            'verbose':
            {
                'format': '%(levelname)s %(asctime)s %(module)s ' +
                          '%(process)d %(thread)d %(message)s'
            },
            'simple':
            {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers':
        {
            'console':
            {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
                'stream': sys.stdout
            },
        },
        'loggers':
        {
            'django':
            {
                'handlers': ['console'],
                'level': 'INFO'
            },
            'gunicorn.access':
            {
                'handlers': ['console'],
                'level': 'DEBUG'
            },
            'gunicorn.error':
            {
                'handlers': ['console'],
                'level': 'INFO'
            }
        }
    }

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (BASE_DIR+'/pageitforward/templates',)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangular',
    'bootstrap3',
    'djangobower',
    'users',
    'orgs',
    'events',
    'eventhandlers',
    'logevent',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pageitforward.urls'
WSGI_APPLICATION = 'pageitforward.wsgi.application'
AUTH_USER_MODEL = 'users.UserData'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# *****************************
# *** Begin Heroku Settings ***
# *****************************

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {}
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)


#BOWER SETTINGS
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."),
)

BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_ROOT+"/pageitforward/static/", 'components')


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

BOWER_INSTALLED_APPS = (
    'angular-local-storage',
)
