"""
Django settings for the GeoLing project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/


Authors:
- Damir Cavar <damir@linguistlist.org>
- Lwin Moe <lwin@linguistlist.org>

"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# TODO: add your secret key here
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

import secret
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = secret.DEBUG

ADMINS = (
    #('Admin', 'errors@linguistlist.org'),
)

MANAGERS = ADMINS

# TODO: add your allowed hosts here
ALLOWED_HOSTS = ['.xyz.org', 'localhost']

ugettext_lazy = lambda s: s
LANGUAGES = (
  ('en', 'English'),
  ('de', 'Deutsch'),
  ('es', 'Español'),
  ('fr', 'Français'),
  ('zh-cn', '汉语'),
  ('ru', 'Русский'),
  ('my', 'မြန်မာ'),
  ('pl', 'Polski'),
  ('ar', 'العربية'),
  ('hr', 'Hrvatski'),
  ('ojb', 'Ojibwe'),
  ('lkt', 'Lakota'),
  ('iw', 'עברית'),
  ('ji', 'Yidish'),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

if DEBUG:
    # dummy cache for development
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    # cache for production server
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'TIMEOUT': 300,
        }
    }

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                #'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },

    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, 'assets')
MEDIA_URL = '/assets/'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'taggit',
    'geoevent',
)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'geoling.urls'

WSGI_APPLICATION = 'geoling.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': secret.DATABASE_ENGINE,
        'NAME': secret.DATABASE_NAME,
        'USER': secret.DATABASE_USER,
        'PASSWORD': secret.DATABASE_PASS,
        'HOST': secret.DATABASE_HOST,
        'PORT': secret.DATABASE_PORT,
        'CONN_MAX_AGE': None, #for unlimited persistent connections, per Damir. Was 600 before.
    }
}

import sys
if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}
    # TODO: set your database name here (replace DBNAME)
    DATABASES['DBNAME'] = {'ENGINE': 'django.db.backends.sqlite3'}

#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True

# for performance:
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Indianapolis'
USE_I18N = True
USE_L10N = True
USE_TZ = True

RECAPTCHA_PUBLIC=secret.RECAPTCHA_PUBLIC
RECAPTCHA_PRIVATE=secret.RECAPTCHA_PRIVATE
RECAPTCHA_API='https://www.google.com/recaptcha/api/siteverify'

EMAIL_BACKEND = secret.EMAIL_BACKEND
EMAIL_USE_TLS = secret.EMAIL_USE_TLS
EMAIL_HOST = secret.EMAIL_HOST
EMAIL_PORT = secret.EMAIL_PORT
EMAIL_HOST_USER = secret.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secret.EMAIL_HOST_PASSWORD

# TODO: set your default from email address here
DEFAULT_FROM_EMAIL = ''
