import os

from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load = load_dotenv(os.path.join(BASE_DIR, ".env"))

# Variable environment local or production
ENV = os.environ.get("ENV", "development")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "spifgucrnt)heocnegcfi(zye624_2984985@54sd9+fv4-r9v4d9gv4s9r8f4vc9rd4g98",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV != "production"


ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1 localhost").split(" ")
CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS", "http://127.0.0.1 http://localhost"
).split(" ")


# Application definition
DJANGO_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admindocs",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_extensions",
    "drf_yasg",
    "cloudinary",
    "cloudinary_storage",
    "channels",
]

LOCAL_APPS = [
    "apps.home",
    "apps.authentication",
    "apps.profiles",
    "apps.post",
    "apps.comment",
    "apps.follow",
    "apps.notification",
    "apps.bookmark",
    "apps.chat",
]

DEVELOP_APPS = [
    "livereload",
]

if ENV != "production":
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + DEVELOP_APPS
else:
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # whitenoise
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # django cors headers middleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

MIDDLEWARE = (
    MIDDLEWARE + ["livereload.middleware.LiveReloadScript"]
    if ENV != "production"
    else MIDDLEWARE
)


ROOT_URLCONF = "config.urls"


TEMPLATES_DIRS = [
    os.path.join(BASE_DIR, "templates"),
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": TEMPLATES_DIRS,
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
ASGI_APPLICATION = "config.asgi.application"


# Database
TYPE_DATABASE = os.environ.get("TYPE_DATABASE", "sqlite3")

if TYPE_DATABASE == "sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DB_ENGINE"),
            "NAME": os.environ.get("DB_NAME"),
            "USER": os.environ.get("DB_USER"),
            "PASSWORD": os.environ.get("DB_PASSWORD"),
            "HOST": os.environ.get("DB_HOST"),
            "PORT": os.environ.get("DB_PORT"),
        },
    }


if ENV == "production":
    hosts_redis = [
        (
            f"redis://:{os.environ['REDIS_PASSWORD']}@{os.environ['REDIS_HOST']}:{os.environ['REDIS_PORT']}/0"
        )
    ]
else:
    hosts_redis = [
        (os.environ.get("REDIS_HOST", "localhost"), os.environ.get("REDIS_PORT", 6379))
    ]


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": hosts_redis},
    },
}


# Config rest_framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": [
        "apps.utils.renderers.CustomJSONRenderer",
    ],
    # 'NON_FIELD_ERRORS_KEY': 'error',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 2
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
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
LANGUAGE_CODE = "fr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)


STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"
        if ENV == "production"
        else "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

if ENV != "production":
    MEDIA_URL = "/mediafiles/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles/")

if ENV == "production":
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": os.environ["CLOUDINARY_CLOUD_NAME"],
        "API_KEY": os.environ["CLOUDINARY_API_KEY"],
        "API_SECRET": os.environ["CLOUDINARY_API_SECRET"],
    }


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "authentication.User"


# Config Send Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_PORT = os.environ["EMAIL_PORT"]
EMAIL_USE_TLS = os.environ["EMAIL_USE_TLS"]


# settings JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=28),
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "public_id",
    "USER_ID_CLAIM": "public_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
}


# the list of origins authorized to make HTTP requests
CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS", "http://localhost:3000 http://127.0.0.1:3000"
).split(" ")

# Domain name frontend

DOMAIN_FRONTEND = os.environ.get("DOMAIN_FRONTEND", "http://localhost:3000")


DJANGORESIZED_DEFAULT_SIZE = [500, 500]
# DJANGORESIZED_DEFAULT_SCALE = 0.5
DJANGORESIZED_DEFAULT_QUALITY = 90
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = "JPEG"
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {"JPEG": ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True
