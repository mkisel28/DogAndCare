from pathlib import Path
from utils.logging_filters import UserFilter
import os
from datetime import timedelta

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_sdk.init(
    dsn="https://0328d2ada8d386146cb1eacb05d22008@o4508060683206656.ingest.us.sentry.io/4508060685893632",
    integrations=[
        DjangoIntegration(),
        CeleryIntegration(),  # Для интеграции с Celery (если используется)
        LoggingIntegration(level=None, event_level=None),  # Логгирование ошибок
    ],
    traces_sample_rate=1.0,  # Включение трассировки (1.0 - 100% запросов)
    profiles_sample_rate=1.0,
    send_default_pii=True,  # Для отправки данных пользователей (опционально)
    environment="production",  # Указание, что это продакшн
    attach_stacktrace=True,  # Добавление стектрейсов к событиям
    max_breadcrumbs=50,  # Настройка количества breadcrumbs
    max_request_body_size="always",  # Захват данных запроса для улучшенной диагностики
)

BASE_DIR = Path(__file__).resolve().parent.parent


INSTALLED_APPS = [
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # -- REST --
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "drf_spectacular",
    "corsheaders",
    # -- REST --
    "apps.locations",
    "apps.users",
    "apps.authentication",
    "apps.media",
    "apps.api",
    "apps.pets",
    "apps.reminders",
    "apps.health",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "middleware.jwt.JWTUserMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # allauth account middleware
]


ROOT_URLCONF = "config.urls"


CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:3000",
).split(",")

CORS_ALLOW_CREDENTIALS = os.environ.get("CORS_ALLOW_CREDENTIALS", "True").lower() in (
    "true",
    "1",
    "t",
)

CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS",
    "http://localhost:3000",
).split(",")

CORS_ALLOW_ALL_ORIGINS = False


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


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


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

CACHE_TIMEOUT = 3600


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


SPECTACULAR_SETTINGS = {
    "TITLE": "API",
    "DESCRIPTION": "API for Dog&Care",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": "/api/schema",
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "defaultModelRendering": "example",
        "defaultModelsExpandDepth": 2,
        "defaultModelExpandDepth": 2,
    },
}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}


JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "secret")

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=120),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "SIGNING_KEY": JWT_SECRET_KEY,
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=120),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
}

SITE_ID = 1

REST_AUTH = {
    "REST_USE_JWT": True,
    "USE_JWT": True,
    "JWT_AUTH_SECURE": True,
    "REST_SESSION_LOGIN": False,
    "LOGOUT_ON_PASSWORD_CHANGE": False,
    "JWT_AUTH_HTTPONLY": False,
    "USER_DETAILS_SERIALIZER": "apps.api.v1.users.serializer.serializers.UserSerializer",
    "REGISTER_SERIALIZER": "apps.api.v1.authentication.serializer.serializers.CustomRegisterSerializer",
    "LOGIN_SERIALIZER": "apps.api.v1.authentication.serializer.serializers.CustomLoginSerializer",
    "JWT_TOKEN_CLAIMS_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "UNIQUE_EMAIL": True,
    "JWT_AUTH_SAMESITE": "None",
}

REST_USE_JWT = True
# allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED = True
AUTHENTICATION_BACKENDS = (
    "allauth.account.auth_backends.AuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
    "rest_framework_simplejwt.authentication.JWTAuthentication",
)
ACCOUNT_ADAPTER = "config.adapters.AccountAdapter"
LOGIN_REDIRECT_URL = "/"
SOCIALACCOUNT_ENABLED = True
SOCIALACCOUNT_STORE_TOKENS = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "SCOPE": ["email", "profile"],
        "OAUTH_PKCE_ENABLED": True,
    }
}

LOG_DIR = BASE_DIR / "logs"
access_log_dir = LOG_DIR / "access"
info_log_dir = LOG_DIR / "info"
error_log_dir = LOG_DIR / "error"

for log_dir in [LOG_DIR, access_log_dir, info_log_dir, error_log_dir]:
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

LOG_FILE_MAX_SIZE = 5 * 1024 * 1024
LOG_FILE_BACKUP_COUNT = 5

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        "user": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message} {user}",
            "style": "{",
        },
    },
    "filters": {
        "user_filter": {
            "()": UserFilter,
        },
    },
    "handlers": {
        "all": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_DIR / "all.log"),
            "maxBytes": LOG_FILE_MAX_SIZE,
            "backupCount": LOG_FILE_BACKUP_COUNT,
            "formatter": "verbose",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(info_log_dir / "info.log"),
            "maxBytes": LOG_FILE_MAX_SIZE,
            "backupCount": LOG_FILE_BACKUP_COUNT,
            "formatter": "verbose",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(error_log_dir / "errors.log"),
            "maxBytes": LOG_FILE_MAX_SIZE,
            "backupCount": LOG_FILE_BACKUP_COUNT,
            "formatter": "verbose",
        },
        "access_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(access_log_dir / "access.log"),
            "maxBytes": LOG_FILE_MAX_SIZE,
            "backupCount": LOG_FILE_BACKUP_COUNT,
            "formatter": "user",
            "filters": ["user_filter"],
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "sentry": {
            "level": "ERROR",  # только ошибки
            "class": "sentry_sdk.integrations.logging.EventHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["all", "error_file"],
            "level": "INFO",
        },
        "django": {
            "handlers": ["sentry", "file", "console", "error_file", "access_file"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["access_file", "console", "error_file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console", "error_file"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = "mkisel28@gmail.com"
EMAIL_HOST_PASSWORD = "yopf icrp hzoo ztxx"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Redis как брокер сообщений
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
)

# Префикс для задач, чтобы можно было группировать их по проекту
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 минут для задачи
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # Мягкий тайм-аут
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# Настройка отказоустойчивости (retry для задач)
CELERY_RETRY_DELAY = 60
CELERY_MAX_RETRIES = 3
CELERY_ACKS_LATE = True  # задачи будут отмечены выполненными только после завершения

CELERY_WORKER_MAX_TASKS_PER_CHILD = (
    1000  # Перезапуск воркера после 1000 задач (защита от утечек памяти)
)
CELERY_WORKER_CONCURRENCY = 4  # Число воркеров

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "UTC"


try:
    from .local_settings import *
    if DEBUG:
        INTERNAL_IPS = [
            "127.0.0.1",
        ]

        INSTALLED_APPS += [
            "debug_toolbar",
        ]

        MIDDLEWARE += [
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        ]

        import socket

        hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
        INTERNAL_IPS += [ip[: ip.rfind(".")] + ".1" for ip in ips]

        DEBUG_TOOLBAR_CONFIG = {
            "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
        }


except ImportError:
    print("No local settings found")
    from .prod_settings import *
