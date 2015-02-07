"""
Django settings for edito313 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/

WARNING: THIS FILE STORES ONLY DEFAULTS. EACH PROJECT MUST HAVE IT'S
         OWN SETTINGS.PY!
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get('DEBUG', False):
    DEBUG = True
else:
    DEBUG = False

TEMPLATE_DEBUG = DEBUG

if DEBUG and not os.environ.get('SITEPATH', False):
    os.environ['SITEPATH'] = os.path.join(os.path.dirname(__file__), 'test')

# Initiate the plugin architecture
from plugin import discover

# Website's base directory. It's been defined by an environment variable prior
# to WSGI init or at the wsgi.py script.
BASE_DIR = os.environ.get('SITEPATH', '.')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# TODO: Generate secret key for each project
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2tkm=n)5bhv8q67bb708n+_hu&hs3vcuz$_4d7avfsqp!r!!48'

ALLOWED_HOSTS = []

# Each site will use it's own database, so they'll always be #1
SITE_ID = 1

# Application definition

# (Use os.environ('SITEPATH')
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.webdesign',
    'django_comments',
    'taggit',
    'djangospam',
    'edito313.content',
    'edito313',
) + tuple(discover.DownloadedPlugin.active)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djangospam.cookie.middleware.SpamCookieMiddleware',
)

ROOT_URLCONF = 'edito313.urls'

WSGI_APPLICATION = 'edito313.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.path.dirname(__file__), 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
