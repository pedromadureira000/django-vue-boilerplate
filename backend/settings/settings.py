"""
Django settings.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from functools import partial
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import dj_database_url
from decouple import config, Csv
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

ADMIN_ENABLED = DEBUG

# Auth User model
AUTH_USER_MODEL = 'core.User'

ROLEPERMISSIONS_MODULE = 'core.roles'


# Application definition

INSTALLED_APPS = [
    'core',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'anymail',
    'axes',
    'rest_framework',
    'djoser',
    'rest_framework.authtoken',
    'rolepermissions',
    'django_cpf_cnpj',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'settings.urls'

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

AUTHENTICATION_BACKENDS = [
    # AxesBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesBackend',

    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication', 'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

WSGI_APPLICATION = 'settings.wsgi.application'

DJOSER = {
        "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
        "EMAIL": {
            "password_reset": "core.email.PasswordResetEmail"
        },
        "PERMISSIONS":{
            'password_reset': ['rest_framework.permissions.AllowAny'],
            'password_reset_confirm': ['rest_framework.permissions.AllowAny'],
            'activation': ['rest_framework.permissions.IsAdminUser'],
            'set_password': ['rest_framework.permissions.IsAdminUser'],
            'username_reset': ['rest_framework.permissions.IsAdminUser'],
            'username_reset_confirm': ['rest_framework.permissions.IsAdminUser'],
            'set_username': ['rest_framework.permissions.IsAdminUser'],
            'user_create': ['rest_framework.permissions.IsAdminUser'],
            'user_delete': ['rest_framework.permissions.IsAdminUser'],
            'user': ['rest_framework.permissions.IsAdminUser'],
            'user_list': ['rest_framework.permissions.IsAdminUser'],
            'token_create': ['rest_framework.permissions.IsAdminUser'],
            'token_destroy': ['rest_framework.permissions.IsAdminUser'],

        }
    }


# SMTP
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    DEFAULT_FROM_EMAIL = "webmaster@localhost"
    EMAIL_HOST = "localhost"
    EMAIL_PORT = "1025"
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    EMAIL_USE_TLS = False

else: 
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
    SERVER_EMAIL = config('SERVER_EMAIL')
    ANYMAIL = {'MAILGUN_API_KEY': config('MAILGUN_API_KEY'),
               'MAILGUN_SENDER_DOMAIN': config('MAILGUN_SENDER_DOMAIN'),
               }


# Sentry

SENTRY_DSN = config('SENTRY_DSN', default=None)
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

default_db_url = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

parse_database = partial(dj_database_url.parse, conn_max_age=600)

DATABASES = {
    'default': config('DATABASE_URL', default=default_db_url, cast=parse_database)
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')


# axex
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = datetime.timedelta(seconds=5)
AXES_ONLY_USER_FAILURES = True

# Session age: 60s * 60m * 24h * 7d
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7
