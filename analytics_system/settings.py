"""
Django settings for analytics_system project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from .config import *
from celery.schedules import crontab

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k2uuq8w9$%epynk6jyzqv^&zn%c%q&-e!93tgfsth7_73a*dia'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djgeojson',
    'leaflet',
    'mathfilters',
    'dashboard',
    'corsheaders',
    'logs_api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'analytics_system.urls'

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

WSGI_APPLICATION = 'analytics_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # Default database
    'default': {
        'ENGINE': 'djongo',
        'NAME': MongoDB,
    },
    # Database used for authentication
    'spoken': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': '',                            # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',
    },
}

DATABASE_ROUTERS = [
    # Router to use 'spoken' database for authentications
    'dashboard.router.AuthRouter',
]

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1:8000",
    "http://192.168.100.6:8000",
    "http://192.168.43.71:8000",
]

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_IMPORTS = (
    'dashboard.logsUtil_calcAvg',
    'dashboard.logsUtil_calcEventStats',
    'dashboard.logsUtil_calcFossStats',
    'dashboard.logsUtil_calcISP',
    'dashboard.logsUtil_calcLocStats',
    'dashboard.logsUtil_daily',
    'dashboard.logsUtil_monthly',
    'dashboard.logsUtil_weekly',
    'dashboard.logsUtil_yearly',
)

# Other Celery settings
CELERY_BEAT_SCHEDULE = {
    'daily': {
        'task': 'dashboard.logsUtil_daily.daily',
        'schedule': crontab(minute=0, hour=0),  # execute daily at midnight
    },
    'weekly': {
        'task': 'dashboard.logsUtil_weekly.weekly',
        'schedule': crontab(minute=0, hour=0, day_of_week='sun'),  # execute every Sunday, at 12am
    },
    'monthly': {
        'task': 'dashboard.logsUtil_monthly.monthly',
        'schedule': crontab(minute=0, hour=0, day_of_month='1'),  # execute on the first day of every month,
                                                                  # at 12am
    },
    'yearly': {
        'task': 'dashboard.logsUtil_yearly.yearly',
        'schedule': crontab(minute=0, hour=0, day_of_month='1', month_of_year='1'),  # execute on 1st Jan,
                                                                                     # at 12am every year.
    },
    'calc_avg': {
        'task': 'dashboard.logsUtil_calcAvg.calc_avg',
        'schedule': crontab(minute=0, hour=0),  # everyday at 12am.
    },
    'calc_event_stats': {
        'task': 'dashboard.logsUtil_calcEventStats.calc_event_stats',
        'schedule': crontab(minute=0, hour=0),  # everyday at 12am
    },
    'calc_foss_stats': {
        'task': 'dashboard.logsUtil_calcFossStats.calc_foss_stats',
        'schedule': crontab(minute=0, hour=0),  # everyday at 12am
    },
    'calc_ISP': {
        'task': 'dashboard.logsUtil_calcISP.calc_ISP',
        'schedule': crontab(minute=0, hour=0),  # everyday at 12am
    },
    'calc_loc_stats': {
        'task': 'dashboard.logsUtil_calcLocStats.calc_loc_stats',
        'schedule': crontab(minute=0, hour=0),  # everyday at 12am
    },
}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GEOIP_PATH  = BASE_DIR + '/geodb/'

USE_MIDDLEWARE_LOGS = False  # whether to use middleware logs or client-side JS logs system

SAVE_LOGS_WITH_CELERY = False

MONGO_BULK_INSERT_COUNT = 1  # change to 10000 later

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (20.5937, 78.9629),
    'DEFAULT_ZOOM': 4,
}
