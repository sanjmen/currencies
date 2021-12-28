"""
Django settings for this project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import re
import environ

ROOT_DIR = environ.Path(__file__) - 3  # (<project>/config/settings/common.py - 3 = <project>/)
APPS_DIR = ROOT_DIR.path("apps")

env = environ.Env()
environ.Env.read_env(env_file="config/settings/.env")  # reading .env file


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env.bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["127.0.0.1"])

INTERNAL_IPS = env.list("DJANGO_INTERNAL_IPS", default=["127.0.0.1"])

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

# Put your third-party apps here
THIRD_PARTY_APPS = [
    "django_extensions",
]

# Put your project-specific apps here
PROJECT_APPS = [
    "apps.core.apps.CoreConfig",
    "apps.taskapp.celery.TaskappConfig",
    "apps.markets.apps.MarketsApp"
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(ROOT_DIR.path("templates"))],
        "OPTIONS": {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            "debug": DEBUG,
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {"default": env.db("DJANGO_DATABASE_URL", default="sqlite:///db.sqlite3")}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = str(ROOT_DIR.path("staticfiles"))
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    str(ROOT_DIR.path("static")),
]

MEDIA_ROOT = str(ROOT_DIR.path("media"))
MEDIA_URL = "/media/"

# Location of root django.contrib.admin URL
ADMIN_URL = re.sub("^/", "^", env("DJANGO_ADMIN_URL", default="^admin/"))

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django sites
SITE_ID = 1

# Celery setup (using redis)
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="amqp://")

# Specify a Celery queue to route the tasks to: this will help to see all tasks
# in a queue separated from other tasks of your project
CELERY_TASK_QUEUES = {
    "celery": {"exchange": "celery", "binding_key": "celery"},
    "debug_task": {
        "exchage": "debug_task",
        "binding_key": "debug_task",
    }
}

CELERY_TASK_ROUTES = {
    # BARS
    "apps.taskapp.celery.debug_task": {
        "queue": "debug_task",
        "exchange": "debug_task",
    },
}

DEFAULT_EXCHANGE = 'binance'