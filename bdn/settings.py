"""
Django settings for bdn project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import glob
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9@=u@c78ut26h+%s0_r7+7oyy0ax*dci7xnd&a3b=4xkvxz!6v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '192.168.99.100',
    'localhost',
    '127.0.0.1',
    'app.os.university',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'django_celery_beat',
    'notifications',
    'bdn.notifications_extensions',
    'channels',
    'ajax_select',
    'haystack',
    'rest_framework',
    'corsheaders',
    'mail_templated',
    'bdn.auth',
    'bdn.industry',
    'bdn.certificate',
    'bdn.company',
    'bdn.course',
    'bdn.skill',
    'bdn.provider',
    'bdn.profiles',
    'bdn.job',
    'bdn.verification',
    'bdn.messaging',
    'bdn.connection',
    'bdn.transaction',
    'bdn.job_application',
]

# Import all apps from apps folder
extra_apps_init = glob.glob(
    os.path.join(BASE_DIR, "apps/*/*/__init__.py"))
for extra_app_init in extra_apps_init:
    package_path = '/'.join(extra_app_init.split('/')[:-2])
    if package_path not in sys.path:
        sys.path.append(package_path)
    package_name = extra_app_init.split('/')[-2]
    INSTALLED_APPS += [package_name]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Should be after SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CORS_ALLOW_HEADERS = (
    'Auth-Signature',
    'Auth-Eth-Address',
    'Content-Type',
    'Profile-Type',
)

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'bdn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

ASGI_APPLICATION = "bdn.routing.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', os.environ.get('POSTGRES_SERVICE_HOST', 'db')),
        'PORT': int(os.environ.get('DB_PORT', os.environ.get('POSTGRES_SERVICE_PORT', '5432'))),
    }
}


# ElasticSearch

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': (
            'haystack.backends.elasticsearch2_backend'
            '.Elasticsearch2SearchEngine'
        ),
        'URL': 'http://elasticsearch:9200/',
        'INDEX_NAME': 'haystack',
    },
}


# Django notifications

DJANGO_NOTIFICATIONS_CONFIG = {
    'USE_JSONFIELD': True
}


# Redis

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', '6379'))
REDIS_DB = int(os.environ.get('REDIS_DB', '0'))

# Channels

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

# Celery

CELERY_BROKER_URL = 'redis://{}:{}/{}'.format(REDIS_HOST, REDIS_PORT, REDIS_DB)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'bdn.auth.signature_authentication.SignatureAuthentication',
    )
}


AUTH_USER_MODEL = 'bdn_auth.User'
AUTH_USER_ADMIN = 'bdn_auth.UserAdmin'


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'bdn.storage.WhiteNoiseStaticFilesStorage'

# Email settings
EMAIL_HOST = 'smtp'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'localsmtp'
EMAIL_HOST_PASSWORD = 'localsmtp'


try:
    from .local_settings import *
except ImportError:
    pass
