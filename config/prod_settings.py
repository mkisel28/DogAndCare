from pathlib import Path
from django.utils.translation import gettext_lazy as _
import os


BASE_DIR = Path(__file__).resolve().parent.parent


def str_to_bool(value: str) -> bool:
    """Преобразует строку 'True'/'False' в булево значение."""
    return value.lower() in ("true", "1", "yes")


SECRET_KEY = "django-insecure-7v@5@hz@iya)n2^^5zn#y8ues%y8gi5c^#+47px^2k*)6f9by9"

DEBUG = str_to_bool(os.environ.get("DJANGO_DEBUG", "False"))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("DB_NAME", "dog_care"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "Maksim2001"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", 5432),
        "CONN_MAX_AGE": 600,
    }
}

STATIC_URL = "/dj_static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/dj_media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

LANGUAGE_CODE = "ru"

LANGUAGES = (
    ("ru", _("Russian")),
    ("en", _("English")),
)

LOCALE_PATHS = [
    BASE_DIR / "locale/",
]

USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = "UTC"
