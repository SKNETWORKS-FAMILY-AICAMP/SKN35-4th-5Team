"""
뷰렛 Django 설정.

값은 모두 환경변수에서 읽는다. 로컬은 web/.env (없으면 저장소 루트 .env),
서버는 docker-compose의 env_file로 주입한다. 목록은 web/.env.example 참고.
"""
import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")


def env_str(name: str, default: str = "") -> str:
    """.env.example 을 복사하면 `KEY=` 처럼 빈 값이 생기므로, 빈 값도 기본값으로 처리한다."""
    return os.getenv(name, "").strip() or default


def env_bool(name: str, default: bool = False) -> bool:
    return env_str(name, str(default)).lower() in {"1", "true", "yes", "on"}


def env_list(name: str, default: str = "") -> list[str]:
    return [item.strip() for item in env_str(name, default).split(",") if item.strip()]


DEBUG = env_bool("DJANGO_DEBUG", True)

# 운영(DEBUG=False)에서는 반드시 환경변수로 지정한다.
SECRET_KEY = env_str("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if not DEBUG:
        raise RuntimeError("DJANGO_SECRET_KEY 환경변수가 필요합니다.")
    SECRET_KEY = "django-insecure-local-dev-only"

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

# FastAPI AI 서버 주소. 로컬은 localhost:8000, docker-compose에서는 http://api:8000
AI_API_URL = env_str("AI_API_URL", "http://localhost:8000").rstrip("/")
AI_API_TIMEOUT = float(env_str("AI_API_TIMEOUT", "180"))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "accounts",
    "products",
    "reviews",
    "chat",
]

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
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"

# DATABASE_URL 예: postgres://user:pass@db:5432/beaurette (없으면 로컬 SQLite)
# dj_database_url.config() 는 DATABASE_URL= (빈 값)이면 기본값 대신 {} 를 돌려주므로 직접 parse 한다.
DATABASES = {
    "default": dj_database_url.parse(
        env_str("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
# collectstatic 결과. Nginx가 이 폴더를 /static/ 으로 서빙한다.
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"

# Nginx 뒤에서 HTTPS를 쓸 때 원래 프로토콜을 인식하도록 한다.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# 도메인+HTTPS를 붙인 뒤 True로 켠다. HTTP(IP 접속)에서 켜면 로그인이 안 된다.
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = env_bool("DJANGO_HTTPS", False)
