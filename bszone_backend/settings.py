from pathlib import Path
import os
import shutil
from datetime import timedelta
from urllib.parse import urlsplit

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


load_dotenv(BASE_DIR / ".env")


def csv_env(name: str, default: str) -> list[str]:
    return [item.strip() for item in os.getenv(name, default).split(",") if item.strip()]


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    items: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            items.append(value)
    return items


def normalize_origin(value: str) -> str:
    value = value.strip()
    if not value:
        return ""

    parsed = urlsplit(value)
    if parsed.scheme and parsed.netloc:
        return f"{parsed.scheme}://{parsed.netloc}"

    return value.rstrip("/")


def normalize_host(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if value == "*":
        return value

    parsed = urlsplit(value)
    if parsed.hostname:
        return parsed.hostname

    return value.rstrip("/").split("/")[0].split(":")[0]

SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-dev-secret-key")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

frontend_origins = unique(
    [
        normalize_origin(item)
        for item in csv_env("FRONTEND_URL", "http://localhost:3000")
    ]
)

vercel_hosts = unique(
    [
        normalize_host(os.getenv("VERCEL_URL", "")),
        normalize_host(os.getenv("VERCEL_BRANCH_URL", "")),
        normalize_host(os.getenv("VERCEL_PROJECT_PRODUCTION_URL", "")),
    ]
)

allowed_hosts = unique(
    [normalize_host(item) for item in csv_env("DJANGO_ALLOWED_HOSTS", "")]
    + vercel_hosts
)
ALLOWED_HOSTS = allowed_hosts or ["*"]
CSRF_TRUSTED_ORIGINS = unique(
    [
        normalize_origin(item)
        for item in csv_env(
            "DJANGO_CSRF_TRUSTED_ORIGINS",
            ",".join(frontend_origins) or "http://localhost:3000",
        )
    ]
)
CORS_ALLOWED_ORIGINS = frontend_origins
CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "common",
    "users",
    "land",
    "employee",
    "worklog",
    "vehicle",
    "sales",
    "expenses",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "srk_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "srk_backend.wsgi.application"
ASGI_APPLICATION = "srk_backend.asgi.application"


def default_database_url() -> str:
    bundled_sqlite_path = BASE_DIR / "db.sqlite3"

    # Vercel functions have a read-only deployment filesystem but a writable /tmp.
    # If DATABASE_URL is not configured yet, copy the bundled demo sqlite database
    # into /tmp so login and demo writes can still work during deployment previews.
    if str(BASE_DIR).startswith("/var/task") and Path("/tmp").exists():
        runtime_sqlite_path = Path("/tmp") / bundled_sqlite_path.name
        if bundled_sqlite_path.exists() and not runtime_sqlite_path.exists():
            shutil.copyfile(bundled_sqlite_path, runtime_sqlite_path)
        return f"sqlite:///{runtime_sqlite_path}"

    return f"sqlite:///{bundled_sqlite_path}"


database_url = os.getenv("DATABASE_URL", default_database_url())
database_config = dj_database_url.parse(database_url, conn_max_age=600)
if database_config.get("ENGINE") != "django.db.backends.sqlite3" and not DEBUG:
    database_config.setdefault("OPTIONS", {})
    database_config["OPTIONS"]["sslmode"] = "require"

DATABASES = {
    "default": database_config
}

AUTH_PASSWORD_VALIDATORS = []

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "EXCEPTION_HANDLER": "common.exceptions.workspace_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "common.pagination.StandardResultsSetPagination",
    "PAGE_SIZE": 20,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=8),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
