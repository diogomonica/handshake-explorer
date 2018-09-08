"""
Django settings for hsdexplorer project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'du+i%ns0t&4oea8ryrkvw6x5l*2srs#(jrrj)d67k5wg5*$4%0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['testnet.hnsxplorer.com', 'hnsxplorer.com', 'k8s-healthcheck', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sass_processor',
    'explorer',
    'tz_detect',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hsdexplorer.middleware.health.HealthCheckMiddleware',
    'tz_detect.middleware.TimezoneMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'hsdexplorer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hsdexplorer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hnsxplorer_dev',
        'USER': 'hnsxplorer_dev',
        'PASSWORD': None,
        'HOST': 'postgres.infra',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
SESSION_COOKIE_HTTPONLY = True
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_FINDERS =  [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

OPEN_PERIOD = 73
BIDDING_PERIOD = 288
REVEAL_PERIOD = 576

HSD_URI = 'http://handshake-node:13037'

# Celery
CELERY_REDIS_HOST = 'redis'
CELERY_REDIS_PORT = 6379

DATABASES['default']['PASSWORD'] = os.environ.get('DB_PASSWORD')

if os.environ.get('ENV') == 'local':
    DEBUG = True
    ALLOWED_HOSTS.append('localhost')
    ALLOWED_HOSTS.append('192.168.1.9')
    HSD_URI = 'http://localhost:13037'
    CELERY_REDIS_HOST = 'localhost'
    CELERY_REDIS_PORT = 6379
    DATABASES['default']['HOST'] = 'localhost'
    DATABASES['default']['PASSWORD'] = 'password'
    INTERNAL_IPS = ['192.168.1.18', '192.168.1.36']
elif os.environ.get('ENV') == 'testnet':
    DATABASES['default']['NAME'] = 'hnsxplorer_testnet'
    DATABASES['default']['USER'] = 'hnsxplorer_testnet'
elif os.environ.get('ENV') == 'mainnet':
    DATABASES['default']['NAME'] = 'hnsxplorer_mainnet'
    DATABASES['default']['USER'] = 'hnsxplorer_mainnet'

CELERY_BROKER_URL = 'redis://{}:{}'.format(CELERY_REDIS_HOST, CELERY_REDIS_PORT)
CELERY_RESULT_BACKEND = 'redis://{}:{}'.format(CELERY_REDIS_HOST, CELERY_REDIS_PORT)
