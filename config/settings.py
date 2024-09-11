from pathlib import Path
from utils.logging_filters import UserFilter
import os
from datetime import timedelta


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
    "drf_spectacular",
    "corsheaders",
    # -- REST --
    "apps.locations",
    "apps.users",
    "apps.media",
    "apps.api",
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
    "allauth.account.middleware.AccountMiddleware",
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

CACHE_TIMEOUT = 3600  # 1 час


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
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": JWT_SECRET_KEY,
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=120),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

SITE_ID = 1

REST_AUTH = {
    "REST_USE_JWT": True,
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "access-token",
    "JWT_AUTH_REFRESH_COOKIE": "refresh-token",
    "JWT_AUTH_SECURE": True,
    "REST_SESSION_LOGIN": False,
    "LOGOUT_ON_PASSWORD_CHANGE": False,
    "JWT_AUTH_HTTPONLY": True,
    "USER_DETAILS_SERIALIZER": "apps.api.v1.users.serializer.serializers.UserSerializer",
    "REGISTER_SERIALIZER": "apps.api.v1.users.serializer.serializers.CustomRegisterSerializer",
    "UNIQUE_EMAIL": True,
    "JWT_AUTH_SAMESITE": "None",
}

REST_USE_JWT = True
# Настройка allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = "none"


GEOIP_PATH = os.path.join(BASE_DIR, "GeoLite2-City.mmdb")


NBRB_API_URL = os.environ.get(
    "NBRB_API_URL", "https://api.nbrb.by/exrates/rates?periodicity=0"
)
CURRENCIES = os.environ.get("CURRENCIES", "USD,EUR,RUB").split(",")


LOG_DIR = BASE_DIR / "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

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
            "filename": os.path.join(LOG_DIR, "all.log"),
            "maxBytes": LOG_FILE_MAX_SIZE,
            "backupCount": LOG_FILE_BACKUP_COUNT,
            "formatter": "verbose",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "info.log"),
            "maxBytes": LOG_FILE_MAX_SIZE,
            "backupCount": LOG_FILE_BACKUP_COUNT,
            "formatter": "verbose",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "errors.log"),
            "maxBytes": LOG_FILE_MAX_SIZE,
            "backupCount": LOG_FILE_BACKUP_COUNT,
            "formatter": "verbose",
        },
        "access_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "access.log"),
            "maxBytes": LOG_FILE_MAX_SIZE,
            "backupCount": LOG_FILE_BACKUP_COUNT,
            "formatter": "user",
            "filters": ["user_filter"],
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "": {
            "handlers": ["all", "error_file"],
            "level": "INFO",
        },
        "django": {
            "handlers": ["file", "console", "error_file", "access_file"],
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

try:
    from .local_settings import *
except ImportError:
    print("No local settings found")
    from .prod_settings import *
